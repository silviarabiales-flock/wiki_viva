"""Flujo de una consulta. Emite eventos (etapa / resultado) que la API envía por SSE o
resume en un solo JSON."""
from __future__ import annotations

import asyncio
import uuid
from typing import AsyncIterator

from ..motor.wiki import SIN_INFO, Wiki, a_segundos, hhmmss
from ..videos import url_en_segundo
from .base import Afirmacion, ProveedorAgentes


def _etapa(nombre: str, estado: str) -> tuple[str, dict]:
    return "etapa", {"etapa": nombre, "estado": estado}


class Orquestador:
    def __init__(self, wiki: Wiki, agentes: ProveedorAgentes, links_videos):
        self.wiki, self.agentes = wiki, agentes
        self._links = links_videos  # callable -> dict video_id -> url

    def _citas(self, afirmaciones: list[Afirmacion], agente: str, prefijo: str) -> list[dict]:
        """Verificación: solo pasan las afirmaciones cuyo minuto existe en el documento citado."""
        links, out = self._links(), []
        for a in afirmaciones:
            if not a.texto or not self.wiki.minuto_valido(a.video_id, a.minuto):
                continue
            doc = self.wiki.documentos[a.video_id]
            seg = a_segundos(a.minuto)
            sec = doc.seccion_de_segundo(seg)
            out.append({"id": f"{prefijo}{len(out) + 1}", "agente": agente, "video_id": doc.id, "titulo": doc.titulo,
                        "seccion": sec.titulo if sec else "", "minuto": hhmmss(a.minuto), "segundos": seg,
                        "texto": a.texto, "url_video": url_en_segundo(links.get(doc.id), seg),
                        "ficha_id": a.ficha_id if a.ficha_id in self.wiki.fichas else None})
        return out

    def _sin_info(self, cid: str, pregunta: str, vista: str) -> dict:
        return {"consulta_id": cid, "pregunta": pregunta, "vista": vista, "sin_informacion": True,
                "respuesta": SIN_INFO, "vista_funcional": None, "vista_tecnica": None, "citas": [],
                "modo_agentes": self.agentes.modo}

    async def consultar(self, pregunta: str, vista: str = "ambas") -> AsyncIterator[tuple[str, dict]]:
        cid = "c_" + uuid.uuid4().hex[:12]
        correr_f, correr_t = vista != "tecnica", vista != "funcional"

        yield _etapa("busqueda", "en_curso")
        hits = self.wiki.buscar(pregunta)
        if not hits:
            alternativa = await self.agentes.reformular(pregunta, self.wiki.jerga)
            if alternativa:
                hits = self.wiki.buscar(alternativa)
        yield _etapa("busqueda", "listo")
        if not hits:
            yield "resultado", self._sin_info(cid, pregunta, vista)
            return

        contexto = self.wiki.contexto(hits)
        yield _etapa("funcional", "en_curso" if correr_f else "omitida")
        yield _etapa("tecnico", "en_curso" if correr_t else "omitida")

        async def nada():
            return []

        tf = asyncio.create_task(self.agentes.funcional(pregunta, contexto, hits) if correr_f else nada())
        tt = asyncio.create_task(self.agentes.tecnico(pregunta, contexto, hits) if correr_t else nada())
        pendientes = {tf: "funcional", tt: "tecnico"}
        while pendientes:
            hechas, _ = await asyncio.wait(pendientes, return_when=asyncio.FIRST_COMPLETED)
            for t in hechas:
                nombre = pendientes.pop(t)
                t.result()  # propaga errores del agente
                if (nombre == "funcional" and correr_f) or (nombre == "tecnico" and correr_t):
                    yield _etapa(nombre, "listo")

        yield _etapa("verificacion", "en_curso")
        citas = self._citas(tf.result(), "funcional", "F") + self._citas(tt.result(), "tecnico", "T")
        yield _etapa("verificacion", "listo")
        if not citas:
            yield "resultado", self._sin_info(cid, pregunta, vista)
            return

        yield _etapa("sintesis", "en_curso")
        s = await self.agentes.sintesis(pregunta, citas, vista)
        yield _etapa("sintesis", "listo")
        yield "resultado", {"consulta_id": cid, "pregunta": pregunta, "vista": vista, "sin_informacion": False,
                            "respuesta": s.respuesta, "vista_funcional": s.vista_funcional,
                            "vista_tecnica": s.vista_tecnica, "citas": citas, "modo_agentes": self.agentes.modo}
