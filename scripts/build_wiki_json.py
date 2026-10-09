#!/usr/bin/env python3
"""Genera wiki.json (datos del portal) a partir de un bundle OKF de transcripciones procesadas.
Uso: python build_wiki_json.py <bundle> <salida.json>"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "asistente"))
import consulta_okf as c

# Nombre de la grabación de cada documento (prototipo con datos ficticios).
VIDEOS = {
    "charla-tecnica-modernizacion-modulos-4": "Charla tecnica modernizacion 04.mp4",
    "charla-tecnica-modernizacion-modulos-6": "Charla tecnica modernizacion 06.mp4",
    "capacitacion-validacion-compuesta-campo-fecha-2026-05-12": "Tecnaris - Capacitacion validacion compuesta 20260512.mp4",
    "modernizacion-modulos-revision-avance-2026-06-16": "Revision de avance 20260616 - grupos de negocio.mp4",
}
SIN_PROCESAR = [
    "Charla técnica modernización 01", "Charla técnica modernización 02", "Charla técnica modernización 03",
    "Charla técnica modernización 05", "Charla técnica – 2ª parte (1)", "Charla técnica – 2ª parte (2)",
    "Reunión técnica 2026-02-03", "Reunión técnica 2026-02-10", "Reunión técnica 2026-02-24",
    "Revisión de avance 2026-03-03", "Reunión técnica 2026-03-10", "Reunión técnica 2026-03-17",
    "Revisión de avance 2026-03-24", "Reunión técnica 2026-03-31", "Revisión de avance 2026-04-07",
    "Reunión técnica 2026-04-14", "Revisión de avance 2026-04-21", "Reunión técnica 2026-04-28",
    "Revisión de avance 2026-05-05", "Reunión técnica 2026-05-19", "Acuerdos de trabajo 2026-06-30",
]


def main(bundle, salida):
    docs = []
    for ruta, fm, body in c.documentos_del_bundle(bundle):
        did = os.path.splitext(os.path.basename(ruta))[0]
        temas = c.temas_de(body)
        secs, cur, h2 = [], None, None
        for line in body.splitlines():
            if line.startswith("## "):
                h2 = line[3:].strip(); cur = None
                if h2 in ("Reglas y casos especiales detectados", "Términos detectados", "Resumen"):
                    cur = {"h2": h2, "num": None, "titulo": h2, "lineas": []}; secs.append(cur)
                continue
            m = c.SECTION_RE.match(line) if line.startswith("### ") else None
            if m:
                n = int(m.group(1)) if m.group(1) else None
                tm = temas.get(n, {})
                cur = {"h2": h2, "num": n, "titulo": m.group(2), "desde": m.group(3) or tm.get("desde"),
                       "hasta": m.group(4) or tm.get("hasta"), "dominio": tm.get("dominio", fm.get("dominio")), "lineas": []}
                secs.append(cur); continue
            if cur is not None:
                cur["lineas"].append(line)
        for s in secs:
            s["texto"] = "\n".join(s.pop("lineas")).strip()
        docs.append({"id": did, "titulo": fm["title"], "fecha": fm.get("timestamp"), "duracion": fm.get("duracion"),
                     "dominio": fm.get("dominio"), "descripcion": fm.get("description"),
                     "video": VIDEOS.get(did, did + ".mp4"), "secciones": secs})
    glos = []
    gpath = os.path.join(bundle, "_PLANTILLA_Y_GLOSARIO.md")
    if os.path.exists(gpath):
        for line in open(gpath, encoding="utf-8").read().splitlines():
            m = re.match(r"^\| (.+?) \| (.+?) \| (.*?) \|$", line)
            if m and not line.startswith("| Lo que dice") and not line.startswith("|---") and '"' in m.group(1):
                glos.append({"audio": m.group(1), "es": m.group(2), "nota": m.group(3)})
    data = {"prototipo": True, "documentos": docs, "glosario": glos, "sin_procesar": SIN_PROCESAR}
    json.dump(data, open(salida, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"{salida}: {len(docs)} documentos, {len(glos)} filas de glosario")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
