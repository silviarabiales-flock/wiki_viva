"""API del backend de la Wiki viva. Contrato: docs/api/openapi.yaml"""
from __future__ import annotations

import json
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from .agentes.claude import AgentesClaude
from .agentes.orquestador import Orquestador
from .agentes.simulacion import AgentesSimulados
from .config import VERSION, Config
from .datos.repositorio import Repositorio
from .errores import ApiError, cuerpo_error, registrar_manejadores
from .motor.wiki import Wiki, hhmmss, normalizar
from .seguridad import LimitadorConsultas, Usuario, exigir, usuario_actual
from .videos import url_en_segundo


# ----------------------------------------------------------------- modelos de entrada
class PedidoConsulta(BaseModel):
    pregunta: str = Field(min_length=3, max_length=500)
    vista: Literal["ambas", "funcional", "tecnica"] = "ambas"


class PedidoOpinion(BaseModel):
    util: bool
    comentario: str | None = Field(default=None, max_length=500)


class PedidoEstadoHueco(BaseModel):
    estado: Literal["abierta", "resuelta"]


class LinksVideos(BaseModel):
    links: dict[str, str]


# ----------------------------------------------------------------- app
def crear_app(config: Config | None = None) -> FastAPI:
    cfg = config or Config()

    @asynccontextmanager
    async def ciclo(app: FastAPI):
        yield

    app = FastAPI(title="Wiki viva – API de consulta", version=VERSION, lifespan=ciclo)
    app.state.config = cfg
    app.state.wiki = Wiki(cfg.wiki_dir, cfg.asistente_dir)
    app.state.repo = Repositorio(cfg.db_path)
    if cfg.modo_agentes == "claude":
        agentes = AgentesClaude(cfg.anthropic_api_key, cfg.modelo_agentes, cfg.modelo_sintesis)
    else:
        agentes = AgentesSimulados(cfg.simulacion_demora_ms)
    app.state.orquestador = Orquestador(app.state.wiki, agentes, app.state.repo.links)
    app.state.limitador = LimitadorConsultas(cfg.consultas_por_minuto)

    app.add_middleware(CORSMiddleware, allow_origins=cfg.origenes_permitidos, allow_methods=["GET", "POST", "PATCH", "PUT"],
                       allow_headers=["Authorization", "Content-Type", "Accept", "X-Rol-Dev", "X-Usuario-Dev"])
    registrar_manejadores(app)

    def wiki(request: Request) -> Wiki:
        return request.app.state.wiki

    def repo(request: Request) -> Repositorio:
        return request.app.state.repo

    def video_resumen(d, links) -> dict:
        return {"id": d.id, "titulo": d.titulo, "fecha": d.fecha, "duracion": d.duracion, "dominio": d.dominio,
                "descripcion": d.descripcion, "archivo_video": d.archivo_video, "url_video": links.get(d.id),
                "temas": [{"numero": s.numero, "titulo": s.titulo, "desde": hhmmss(s.desde), "hasta": hhmmss(s.hasta),
                           "dominio": s.dominio} for s in d.temas()]}

    # ------------------------------------------------------------- sistema
    @app.get("/api/salud")
    def salud(request: Request):
        return {"estado": "ok", "modo_agentes": request.app.state.orquestador.agentes.modo,
                "videos": len(request.app.state.wiki.documentos), "fichas": len(request.app.state.wiki.fichas),
                "version": VERSION}

    # ------------------------------------------------------------- consultas
    @app.post("/api/consultas")
    async def consultar(pedido: PedidoConsulta, request: Request, u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        request.app.state.limitador.verificar(u.id)
        orq: Orquestador = request.app.state.orquestador
        rp: Repositorio = request.app.state.repo
        pregunta = pedido.pregunta.strip()

        def cerrar(resultado: dict):
            rp.guardar_consulta(u.id, resultado)
            if resultado["sin_informacion"]:
                rp.registrar_hueco(pregunta)

        if "text/event-stream" in request.headers.get("accept", ""):
            async def eventos():
                try:
                    async for tipo, datos in orq.consultar(pregunta, pedido.vista):
                        if tipo == "resultado":
                            cerrar(datos)
                        yield f"event: {tipo}\ndata: {json.dumps(datos, ensure_ascii=False)}\n\n"
                except ApiError as e:
                    yield f"event: error\ndata: {json.dumps(cuerpo_error(e.codigo, e.mensaje), ensure_ascii=False)}\n\n"
                except Exception:
                    yield f"event: error\ndata: {json.dumps(cuerpo_error('error_interno', 'Ocurrió un error inesperado.'))}\n\n"

            return StreamingResponse(eventos(), media_type="text/event-stream",
                                     headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

        resultado = None
        async for tipo, datos in orq.consultar(pregunta, pedido.vista):
            if tipo == "resultado":
                resultado = datos
        cerrar(resultado)
        return resultado

    @app.post("/api/consultas/{consulta_id}/opinion", status_code=204)
    def opinar(consulta_id: str, pedido: PedidoOpinion, rp: Repositorio = Depends(repo), u: Usuario = Depends(usuario_actual)):
        exigir(u, "colaborador")
        if not rp.existe_consulta(consulta_id):
            raise ApiError(404, "no_encontrado", "No existe esa consulta.")
        rp.guardar_opinion(consulta_id, u.id, pedido.util, pedido.comentario)
        return Response(status_code=204)

    # ------------------------------------------------------------- wiki
    @app.get("/api/wiki/indice")
    def indice(w: Wiki = Depends(wiki), rp: Repositorio = Depends(repo), u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        links = rp.links()
        videos = sorted(w.documentos.values(), key=lambda d: d.fecha or "0000", reverse=True)
        return {"titulo": w.titulo, "videos": [video_resumen(d, links) for d in videos], "sin_procesar": w.sin_procesar,
                "total_fichas": len(w.fichas)}

    @app.get("/api/wiki/videos/{video_id}")
    def video(video_id: str, w: Wiki = Depends(wiki), rp: Repositorio = Depends(repo), u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        d = w.documentos.get(video_id)
        if not d:
            raise ApiError(404, "no_encontrado", "No existe ese video en la wiki.")
        out = video_resumen(d, rp.links())
        out["secciones"] = [{"numero": s.numero, "titulo": s.titulo, "tipo": s.tipo, "desde": hhmmss(s.desde),
                             "hasta": hhmmss(s.hasta), "dominio": s.dominio, "texto": s.texto} for s in d.secciones]
        return out

    @app.get("/api/wiki/fichas")
    def listar_fichas(tipo: Literal["Término", "Regla de negocio", "Caso especial"] | None = None,
                      w: Wiki = Depends(wiki), u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        fichas = sorted(w.fichas.values(), key=lambda f: (f.tipo, normalizar(f.titulo)))
        return {"fichas": [f.resumen() for f in fichas if not tipo or f.tipo == tipo]}

    @app.get("/api/wiki/fichas/{ficha_id}")
    def ver_ficha(ficha_id: str, w: Wiki = Depends(wiki), u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        f = w.fichas.get(ficha_id)
        if not f:
            raise ApiError(404, "no_encontrado", "No existe esa ficha.")
        return {**f.resumen(), "secciones": [{"titulo": s.titulo, "texto": s.texto} for s in f.secciones]}

    @app.get("/api/glosario")
    def glosario(q: str | None = None, w: Wiki = Depends(wiki), u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        terminos, jerga = w.terminos(), w.jerga
        if q:
            f = normalizar(q)
            terminos = [t for t in terminos if f in normalizar(" ".join(str(v) for v in t.values()))]
            jerga = [j for j in jerga if f in normalizar(" ".join(str(v) for v in j.values()))]
        return {"terminos": terminos, "jerga": jerga}

    # ------------------------------------------------------------- huecos
    @app.get("/api/huecos")
    def listar_huecos(estado: Literal["abierta", "resuelta"] | None = None, rp: Repositorio = Depends(repo),
                      u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        return {"huecos": rp.huecos(estado)}

    @app.patch("/api/huecos/{hueco_id}")
    def actualizar_hueco(hueco_id: str, pedido: PedidoEstadoHueco, rp: Repositorio = Depends(repo),
                         u: Usuario = Depends(usuario_actual)):
        exigir(u, "editor")
        if not rp.hueco(hueco_id):
            raise ApiError(404, "no_encontrado", "No existe esa pregunta sin respuesta.")
        return rp.cambiar_estado_hueco(hueco_id, pedido.estado)

    # ------------------------------------------------------------- configuración
    @app.get("/api/config/videos")
    def ver_links(rp: Repositorio = Depends(repo), u: Usuario = Depends(usuario_actual)):
        exigir(u, "lector")
        return {"links": rp.links()}

    @app.put("/api/config/videos")
    def guardar_links(pedido: LinksVideos, w: Wiki = Depends(wiki), rp: Repositorio = Depends(repo),
                      u: Usuario = Depends(usuario_actual)):
        exigir(u, "editor")
        for vid, url in pedido.links.items():
            if vid not in w.documentos:
                raise ApiError(400, "consulta_invalida", f"No existe el video {vid}.")
            if not url_en_segundo(url, 0):
                raise ApiError(400, "consulta_invalida", f"El link de {vid} tiene que empezar con http:// o https://.")
        return {"links": rp.reemplazar_links(pedido.links)}

    return app


app = crear_app()
