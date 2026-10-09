#!/usr/bin/env python3
"""
consulta_okf.py — Motor de consulta sobre un bundle OKF (Open Knowledge Format).

Uso:
  python consulta_okf.py indexar <carpeta_bundle>
      Genera/actualiza <carpeta_bundle>/index.md (punto de entrada OKF).

  python consulta_okf.py buscar <carpeta_bundle> "<pregunta>" [--top N] [--json]
      Recorre el bundle con divulgación progresiva (index.md -> documentos ->
      secciones) y devuelve los fragmentos que responden la pregunta, con el
      timestamp en formato hh:mm:ss. Si nada supera el umbral de evidencia,
      devuelve sin_resultados = true ("No tengo información sobre tu consulta").

Sin dependencias externas (Python 3.8+). Lee YAML simple del frontmatter.
"""
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter

SIN_INFO = "No tengo información sobre tu consulta"

# ----------------------------------------------------------------- utilidades

STOP = set("""
a al algo algun alguna algunas alguno algunos ante antes aqui asi aun bien cada como con
contra cual cuales cuando de del desde donde dos el ella ellas ellos en entre era es esa
esas ese eso esos esta estan estas este esto estos fue ha hay hace hacen hacer hacemos
hago la las le les lo los mas me mi muy no nos o otra otro para pero poco por porque que
quien se ser si sin sobre son su sus tambien te tiene tienen todo todos tu un una unas uno
unos usa usar ya y funciona funcionan significa sirve explica explicar decir dice puedo
puede pueden debo debe deben tengo tenemos quiero necesito cosa caso manera forma
""".split())

TS_RE = re.compile(r"\[(\d{1,2}:\d{2}(?::\d{2})?)")
SECTION_RE = re.compile(r"^###\s+(?:(\d+)\.\s+)?(.+?)\s*(?:\((\d{1,2}:\d{2}(?::\d{2})?)\s*[–-]\s*(\d{1,2}:\d{2}(?::\d{2})?)\))?\s*$")
TEMA_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\w+)\s*\|\s*$")


def sin_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def raiz(tok):
    # Stemming liviano para español: sufijos frecuentes y prefijo de 7 letras.
    for suf in ("aciones", "acion", "iciones", "icion", "ciones", "cion", "adores", "ador",
                "mente", "ados", "adas", "ado", "ada", "ar", "er", "ir", "es", "s"):
        if len(tok) - len(suf) >= 4 and tok.endswith(suf):
            tok = tok[: -len(suf)]
            break
    return tok[:7]


def tokens(texto):
    t = sin_acentos(texto.lower())
    out = []
    for w in re.findall(r"[a-z0-9_]+", t):
        if w in STOP or len(w) < 2:
            continue
        out.append(raiz(w))
    return out


def a_hhmmss(ts):
    """'7:43' -> '00:07:43'; '1:28:26' -> '01:28:26'."""
    if not ts:
        return None
    partes = [int(p) for p in ts.split(":")]
    while len(partes) < 3:
        partes.insert(0, 0)
    h, m, s = partes
    return f"{h:02d}:{m:02d}:{s:02d}"


def a_segundos(ts):
    s = 0
    for p in ts.split(":"):
        s = s * 60 + int(p)
    return s


def slug(texto):
    t = sin_acentos(texto.lower())
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    return re.sub(r"\s+", "-", t.strip())


def leer_frontmatter(texto):
    if not texto.startswith("---"):
        return {}, texto
    fin = texto.find("\n---", 3)
    if fin < 0:
        return {}, texto
    bloque, cuerpo = texto[3:fin], texto[fin + 4:]
    fm = {}
    for linea in bloque.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", linea)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        else:
            v = v.strip('"\'')
        fm[k] = v
    return fm, cuerpo


# ----------------------------------------------------------------- bundle OKF

def documentos_del_bundle(carpeta):
    """Divulgación progresiva: si existe index.md, se siguen sus links; si no, se
    recorren los .md del bundle con frontmatter `type`."""
    idx = os.path.join(carpeta, "index.md")
    rutas = []
    if os.path.exists(idx):
        texto = open(idx, encoding="utf-8").read()
        for link in re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", texto):
            p = os.path.normpath(os.path.join(carpeta, link))
            if os.path.exists(p) and p not in rutas:
                rutas.append(p)
    if not rutas:
        for raiz_dir, _, archivos in os.walk(carpeta):
            for a in sorted(archivos):
                if a.endswith(".md") and a not in ("index.md", "log.md") and not a.startswith("_"):
                    rutas.append(os.path.join(raiz_dir, a))
    docs = []
    for p in rutas:
        fm, cuerpo = leer_frontmatter(open(p, encoding="utf-8").read())
        if fm.get("type"):
            docs.append((p, fm, cuerpo))
    return docs


def temas_de(cuerpo):
    temas = {}
    for linea in cuerpo.splitlines():
        m = TEMA_ROW_RE.match(linea)
        if m and m.group(1).isdigit():
            temas[int(m.group(1))] = {
                "tema": m.group(2), "desde": m.group(3), "hasta": m.group(4), "dominio": m.group(5)}
    return temas


def fragmentos(ruta, fm, cuerpo, carpeta):
    """Corta un documento en fragmentos citables: párrafos/reglas de cada tema,
    filas de términos y reglas sueltas. Cada fragmento lleva su timestamp."""
    temas = temas_de(cuerpo)
    rel = os.path.relpath(ruta, carpeta).replace(os.sep, "/")
    frs = []
    seccion, num, ts_sec, dominio = None, None, None, fm.get("dominio", "")
    heading = None
    bloque_h2 = None
    buffer = []

    def volcar():
        if not buffer:
            return
        texto = "\n".join(buffer).strip()
        buffer.clear()
        if len(texto) < 25:
            return
        ts = TS_RE.search(texto)
        if not ts and texto.startswith("|"):
            ts = re.search(r"(\d{1,2}:\d{2}(?::\d{2})?)", texto.split("|")[-2] if texto.count("|") > 2 else "")
        ts_val = ts.group(1) if ts else ts_sec
        frs.append({
            "doc": rel, "titulo": fm.get("title", rel), "resource": fm.get("resource"),
            "fecha": fm.get("timestamp"), "seccion": seccion or bloque_h2,
            "anchor": slug(heading) if heading else "",
            "timestamp": ts_val, "dominio": dominio, "texto": texto,
            "es_regla": texto.lstrip("> ").startswith("**Regla") or texto.lstrip("> ").startswith("**Caso"),
            "tipo_bloque": "tema" if num else (bloque_h2 or ""),
        })

    for linea in cuerpo.splitlines():
        if linea.startswith("## "):
            volcar()
            bloque_h2, seccion, num, ts_sec = linea[3:].strip(), None, None, None
            heading = bloque_h2
            dominio = fm.get("dominio", "")
            continue
        m = SECTION_RE.match(linea) if linea.startswith("### ") else None
        if m:
            volcar()
            heading = linea[4:].strip()
            num = int(m.group(1)) if m.group(1) else None
            seccion = m.group(2)
            ts_sec = m.group(3) or (temas.get(num, {}).get("desde") if num else None)
            dominio = temas.get(num, {}).get("dominio", fm.get("dominio", ""))
            continue
        if bloque_h2 in ("Temas",) or linea.startswith("# "):
            continue
        # En listas (reglas, pendientes, resumen) y tablas de términos: un fragmento por ítem.
        if bloque_h2 and not num and (linea.startswith("- ") or linea.startswith("| ")):
            volcar()
            if linea.startswith("|---") or linea.startswith("| Término") or linea.startswith("|---"):
                continue
            buffer.append(linea)
            volcar()
            continue
        if not linea.strip():
            volcar()
            continue
        buffer.append(linea)
    volcar()
    # Los "Pendientes" no son respuestas: se marcan para excluirlos.
    for f in frs:
        f["es_pendiente"] = (f["tipo_bloque"] or "").lower().startswith("pendientes")
    return frs


# ----------------------------------------------------------------- búsqueda

def buscar(carpeta, pregunta, top=6):
    docs = documentos_del_bundle(carpeta)
    corpus = []
    for ruta, fm, cuerpo in docs:
        for f in fragmentos(ruta, fm, cuerpo, carpeta):
            if f["es_pendiente"] or not f["timestamp"]:
                continue
            f["_tok"] = tokens(f["texto"]) + tokens(f["seccion"] or "") * 2
            corpus.append(f)

    q = tokens(pregunta)
    if not q or not corpus:
        return {"pregunta": pregunta, "sin_resultados": True, "mensaje": SIN_INFO, "resultados": []}

    N = len(corpus)
    avgdl = sum(len(f["_tok"]) for f in corpus) / N
    df = Counter()
    for f in corpus:
        for t in set(f["_tok"]):
            df[t] += 1
    idf = {t: math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5)) for t in set(q)}

    k1, b = 1.4, 0.75
    qset = set(q)
    puntuados = []
    for f in corpus:
        tf = Counter(f["_tok"])
        dl = len(f["_tok"]) or 1
        s = 0.0
        for t in qset:
            if tf[t]:
                s += idf[t] * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * dl / avgdl))
        cobertura = sum(1 for t in qset if tf[t]) / len(qset)
        if f["es_regla"]:
            s *= 1.15
        puntuados.append((s, cobertura, f))

    puntuados.sort(key=lambda x: -x[0])
    mejor = puntuados[0][0] if puntuados else 0
    # Umbral de evidencia: hace falta puntaje absoluto mínimo y cubrir la mayoría
    # de los conceptos de la pregunta. Si no, "No tengo información".
    UMBRAL_ABS, UMBRAL_COB = 3.0, 0.6
    resultados = []
    for s, cob, f in puntuados:
        if s < UMBRAL_ABS or cob < UMBRAL_COB or s < 0.35 * mejor:
            continue
        resultados.append({
            "puntaje": round(s, 2), "cobertura": round(cob, 2),
            "documento": f["titulo"], "archivo": f["doc"] + (f"#{f['anchor']}" if f["anchor"] else ""),
            "video": f["resource"], "fecha_video": f["fecha"],
            "seccion": f["seccion"], "dominio": f["dominio"],
            "timestamp": a_hhmmss(f["timestamp"]), "texto": f["texto"],
        })
        if len(resultados) >= top:
            break

    # Orden final: por documento y luego cronológico dentro del video.
    resultados.sort(key=lambda r: (r["documento"], a_segundos(r["timestamp"] or "0:00")))
    secciones = {}
    for r in resultados:
        clave = (r["documento"], r["seccion"])
        sec = secciones.setdefault(clave, {"documento": r["documento"], "seccion": r["seccion"],
                                           "archivo": r["archivo"], "dominio": r["dominio"],
                                           "timestamps": [], "puntaje_max": 0})
        if r["timestamp"] not in sec["timestamps"]:
            sec["timestamps"].append(r["timestamp"])
        sec["puntaje_max"] = max(sec["puntaje_max"], r["puntaje"])
    return {
        "pregunta": pregunta,
        "conceptos": sorted(qset),
        "secciones": sorted(secciones.values(), key=lambda x: -x["puntaje_max"]),
        "sin_resultados": not resultados,
        "mensaje": SIN_INFO if not resultados else None,
        "resultados": resultados,
    }


# ----------------------------------------------------------------- index.md

def indexar(carpeta):
    docs = documentos_del_bundle_sin_index(carpeta)
    lineas = [
        "---",
        "type: Índice",
        "title: Wiki viva de consulta de terminología técnica y funcional",
        "description: Punto de entrada OKF. Lista las fuentes (videos procesados) y sus temas con rangos de tiempo para navegar por divulgación progresiva.",
        "tags: [indice]",
        "---",
        "",
        "# Wiki viva de consulta de terminología técnica y funcional",
        "",
        "Cómo navegar: leer este índice, elegir la fuente y el tema, y seguir el link al documento.",
        "Glosario de jerga y errores de transcripción: [_PLANTILLA_Y_GLOSARIO.md](_PLANTILLA_Y_GLOSARIO.md).",
        "",
        "## Fuentes de video",
        "",
    ]
    for ruta, fm, cuerpo in sorted(docs, key=lambda d: d[1].get("timestamp") or "9999"):
        rel = os.path.relpath(ruta, carpeta).replace(os.sep, "/")
        fecha = fm.get("timestamp") or "s/f"
        lineas += [
            f"### [{fm.get('title', rel)}]({rel})",
            "",
            f"- **Fecha:** {fecha} · **Duración:** {fm.get('duracion', '?')} · **Dominio:** {fm.get('dominio', '?')}",
            f"- {fm.get('description', '')}",
            "",
            "| # | Tema | Desde | Hasta | Dominio |",
            "|---|---|---|---|---|",
        ]
        for n, t in sorted(temas_de(cuerpo).items()):
            ancla = slug(f"{n}. {t['tema']} ({t['desde']} – {t['hasta']})")
            lineas.append(f"| {n} | [{t['tema']}]({rel}#{ancla}) | {a_hhmmss(t['desde'])} | {a_hhmmss(t['hasta'])} | {t['dominio']} |")
        lineas.append("")
    with open(os.path.join(carpeta, "index.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lineas))
    return os.path.join(carpeta, "index.md")


def documentos_del_bundle_sin_index(carpeta):
    docs = []
    for raiz_dir, _, archivos in os.walk(carpeta):
        for a in sorted(archivos):
            if a.endswith(".md") and a not in ("index.md", "log.md") and not a.startswith("_"):
                p = os.path.join(raiz_dir, a)
                fm, cuerpo = leer_frontmatter(open(p, encoding="utf-8").read())
                if fm.get("type"):
                    docs.append((p, fm, cuerpo))
    return docs


# ----------------------------------------------------------------- CLI

def imprimir(res):
    print(f"Pregunta: {res['pregunta']}\n")
    if res["sin_resultados"]:
        print(SIN_INFO)
        return
    for r in res["resultados"]:
        print(f"- [{r['timestamp']}] {r['documento']} › {r['seccion']} ({r['dominio']}, puntaje {r['puntaje']})")
        print(f"  {r['archivo']}")
        print("  " + r["texto"].replace("\n", "\n  ")[:600])
        print()


def main(argv):
    if len(argv) < 3 or argv[1] not in ("buscar", "indexar"):
        print(__doc__)
        return 2
    if argv[1] == "indexar":
        print("Índice generado:", indexar(argv[2]))
        return 0
    if len(argv) < 4:
        print(__doc__)
        return 2
    top = 6
    if "--top" in argv:
        top = int(argv[argv.index("--top") + 1])
    res = buscar(argv[2], argv[3], top=top)
    if "--json" in argv:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        imprimir(res)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
