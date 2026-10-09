"""Tests de contrato y preguntas de control (modo simulación, sin API)."""
import json
import re

from .conftest import ROL

SIN_INFO = "No tengo información sobre tu consulta"
VALIDACION = "¿Cómo se hace la validación compuesta?"


def _eventos_sse(texto: str) -> list[tuple[str, dict]]:
    out = []
    for bloque in texto.strip().split("\n\n"):
        tipo = re.search(r"^event: (.+)$", bloque, re.M).group(1)
        datos = json.loads(re.search(r"^data: (.+)$", bloque, re.M).group(1))
        out.append((tipo, datos))
    return out


# ------------------------------------------------------------------ sistema
def test_salud(cliente, contrato):
    r = cliente.get("/api/salud")
    assert r.status_code == 200
    cuerpo = contrato("Salud", r.json())
    assert cuerpo["modo_agentes"] == "simulacion" and cuerpo["videos"] == 4


# ------------------------------------------------------------------ preguntas de control
def test_validacion_compuesta_tiene_respuesta_con_minutos_verificados(cliente, contrato):
    r = cliente.post("/api/consultas", json={"pregunta": VALIDACION}, headers=ROL("lector"))
    assert r.status_code == 200
    res = contrato("ResultadoConsulta", r.json())
    assert res["sin_informacion"] is False
    assert res["citas"], "debería citar al menos un minuto"
    assert any(c["video_id"].startswith("capacitacion-validacion-compuesta") for c in res["citas"])
    # cada cita existe en el documento y cada referencia del texto apunta a una cita
    video = cliente.get(f"/api/wiki/videos/{res['citas'][0]['video_id']}", headers=ROL("lector")).json()
    texto_doc = "\n".join(s["texto"] for s in video["secciones"])
    segundos_doc = {sum(int(p) * 60 ** i for i, p in enumerate(reversed(t.split(":"))))
                    for t in re.findall(r"\b\d{1,2}:\d{2}(?::\d{2})?\b", texto_doc)}
    for c in res["citas"]:
        if c["video_id"] == video["id"]:
            assert c["segundos"] in segundos_doc
        assert re.fullmatch(r"\d{2}:\d{2}:\d{2}", c["minuto"])
    ids = {c["id"] for c in res["citas"]}
    assert set(re.findall(r"\[([FT]\d+)\]", res["respuesta"])) <= ids


def test_pregunta_fuera_de_la_wiki_responde_sin_informacion_y_registra_hueco(cliente, contrato):
    preg = "¿Cuál es la política de vacaciones de la empresa?"
    r = cliente.post("/api/consultas", json={"pregunta": preg}, headers=ROL("lector"))
    res = contrato("ResultadoConsulta", r.json())
    assert res["sin_informacion"] is True and res["respuesta"] == SIN_INFO and res["citas"] == []
    cliente.post("/api/consultas", json={"pregunta": preg}, headers=ROL("lector"))
    huecos = cliente.get("/api/huecos", headers=ROL("lector")).json()["huecos"]
    contrato("Hueco", huecos[0])
    assert huecos[0]["pregunta"] == preg and huecos[0]["veces"] == 2 and huecos[0]["estado"] == "abierta"


def test_jerga_del_audio_se_reformula_con_el_glosario(cliente):
    # "Jason" es como suena JSON en las transcripciones
    r = cliente.post("/api/consultas", json={"pregunta": "¿Qué manda el Front en el Jason?"}, headers=ROL("lector")).json()
    assert r["sin_informacion"] is False


def test_vista_funcional_no_corre_agente_tecnico(cliente):
    r = cliente.post("/api/consultas", json={"pregunta": "¿Qué es un grupo de negocio?", "vista": "funcional"},
                     headers=ROL("lector")).json()
    assert r["sin_informacion"] is False
    assert all(c["agente"] == "funcional" for c in r["citas"]) and r["vista_tecnica"] is None


# ------------------------------------------------------------------ streaming
def test_sse_emite_etapas_en_orden_y_un_resultado(cliente, contrato):
    with cliente.stream("POST", "/api/consultas", json={"pregunta": VALIDACION},
                        headers={**ROL("lector"), "Accept": "text/event-stream"}) as r:
        assert r.status_code == 200 and r.headers["content-type"].startswith("text/event-stream")
        eventos = _eventos_sse(r.read().decode())
    tipos = [t for t, _ in eventos]
    assert tipos[-1] == "resultado" and tipos.count("resultado") == 1
    etapas = [d["etapa"] for t, d in eventos if t == "etapa" and d["estado"] == "listo"]
    assert etapas[0] == "busqueda" and etapas[-2:] == ["verificacion", "sintesis"]
    assert {"funcional", "tecnico"} <= set(etapas)
    contrato("ResultadoConsulta", eventos[-1][1])


def test_sse_sin_informacion_termina_tras_busqueda(cliente):
    with cliente.stream("POST", "/api/consultas", json={"pregunta": "¿Cómo se configura el servidor de correo?"},
                        headers={**ROL("lector"), "Accept": "text/event-stream"}) as r:
        eventos = _eventos_sse(r.read().decode())
    assert [t for t, _ in eventos] == ["etapa", "etapa", "resultado"]
    assert eventos[-1][1]["sin_informacion"] is True


# ------------------------------------------------------------------ validación y errores
def test_pregunta_invalida_devuelve_error_del_contrato(cliente, contrato):
    r = cliente.post("/api/consultas", json={"pregunta": "a"}, headers=ROL("lector"))
    assert r.status_code == 400
    assert contrato("Error", r.json())["error"]["codigo"] == "consulta_invalida"


def test_rol_desconocido_no_autorizado(cliente, contrato):
    r = cliente.get("/api/wiki/indice", headers=ROL("admin"))
    assert r.status_code == 401 and contrato("Error", r.json())["error"]["codigo"] == "no_autorizado"


def test_limite_de_consultas(cliente):
    cliente.app.state.limitador.por_minuto = 2
    for _ in range(2):
        assert cliente.post("/api/consultas", json={"pregunta": VALIDACION}, headers=ROL("lector", "beto")).status_code == 200
    r = cliente.post("/api/consultas", json={"pregunta": VALIDACION}, headers=ROL("lector", "beto"))
    assert r.status_code == 429 and r.json()["error"]["codigo"] == "limite_consultas"


# ------------------------------------------------------------------ wiki
def test_indice_video_y_glosario(cliente, contrato):
    ind = contrato("Indice", cliente.get("/api/wiki/indice", headers=ROL("lector")).json())
    assert ind["titulo"] == "Wiki viva de consulta de terminología técnica y funcional"
    assert len(ind["videos"]) == 4 and ind["sin_procesar"]
    vid = ind["videos"][0]["id"]
    contrato("Video", cliente.get(f"/api/wiki/videos/{vid}", headers=ROL("lector")).json())
    assert cliente.get("/api/wiki/videos/no-existe", headers=ROL("lector")).status_code == 404
    g = contrato("Glosario", cliente.get("/api/glosario", params={"q": "jason"}, headers=ROL("lector")).json())
    assert any("JSON" in j["significado"] for j in g["jerga"])


# ------------------------------------------------------------------ roles: opiniones, huecos, links
def test_opinion_requiere_colaborador(cliente):
    cid = cliente.post("/api/consultas", json={"pregunta": VALIDACION}, headers=ROL("lector")).json()["consulta_id"]
    assert cliente.post(f"/api/consultas/{cid}/opinion", json={"util": True}, headers=ROL("lector")).status_code == 403
    assert cliente.post(f"/api/consultas/{cid}/opinion", json={"util": True}, headers=ROL("colaborador")).status_code == 204
    assert cliente.post("/api/consultas/c_inexistente/opinion", json={"util": True}, headers=ROL("colaborador")).status_code == 404
    assert cliente.app.state.repo.opiniones(cid)[0]["util"] == 1


def test_resolver_hueco_requiere_editor(cliente, contrato):
    cliente.post("/api/consultas", json={"pregunta": "¿Cuál es la política de vacaciones?"}, headers=ROL("lector"))
    hid = cliente.get("/api/huecos", headers=ROL("lector")).json()["huecos"][0]["id"]
    assert cliente.patch(f"/api/huecos/{hid}", json={"estado": "resuelta"}, headers=ROL("colaborador")).status_code == 403
    r = cliente.patch(f"/api/huecos/{hid}", json={"estado": "resuelta"}, headers=ROL("editor"))
    assert contrato("Hueco", r.json())["estado"] == "resuelta"
    assert cliente.get("/api/huecos", params={"estado": "abierta"}, headers=ROL("lector")).json()["huecos"] == []


def test_links_de_videos_y_url_al_segundo(cliente, contrato):
    vid = "capacitacion-validacion-compuesta-campo-fecha-2026-05-12"
    links = {"links": {vid: "https://empresa.sharepoint.com/sites/x/stream.aspx?id=abc"}}
    assert cliente.put("/api/config/videos", json=links, headers=ROL("colaborador")).status_code == 403
    assert cliente.put("/api/config/videos", json={"links": {vid: "ftp://x"}}, headers=ROL("editor")).status_code == 400
    assert cliente.put("/api/config/videos", json={"links": {"no-existe": "https://x"}}, headers=ROL("editor")).status_code == 400
    contrato("LinksVideos", cliente.put("/api/config/videos", json=links, headers=ROL("editor")).json())
    res = cliente.post("/api/consultas", json={"pregunta": VALIDACION}, headers=ROL("lector")).json()
    cita = next(c for c in res["citas"] if c["video_id"] == vid)
    assert "nav=" in cita["url_video"]
