"""Carga del bundle OKF en memoria y búsqueda (reutiliza asistente/consulta_okf.py)."""
from __future__ import annotations

import importlib.util
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

TS_RE = re.compile(r"\b(\d{1,2}:\d{2}(?::\d{2})?)\b")
SIN_INFO = "No tengo información sobre tu consulta"

ARCHIVO_VIDEO = {  # nombre de la grabación de cada documento (prototipo, datos ficticios)
    "charla-tecnica-modernizacion-modulos-4": "Charla tecnica modernizacion 04.mp4",
    "charla-tecnica-modernizacion-modulos-6": "Charla tecnica modernizacion 06.mp4",
    "capacitacion-validacion-compuesta-campo-fecha-2026-05-12": "Tecnaris - Capacitacion validacion compuesta 20260512.mp4",
    "modernizacion-modulos-revision-avance-2026-06-16": "Revision de avance 20260616 - grupos de negocio.mp4",
}


def cargar_motor(asistente_dir: Path):
    spec = importlib.util.spec_from_file_location("consulta_okf", asistente_dir / "consulta_okf.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def a_segundos(ts: str) -> int:
    s = 0
    for p in ts.split(":"):
        s = s * 60 + int(p)
    return s


def hhmmss(ts: str | None) -> str | None:
    if not ts:
        return None
    s = a_segundos(ts)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


@dataclass
class Seccion:
    numero: int | None
    titulo: str
    tipo: str  # tema | resumen | terminos | reglas
    texto: str
    desde: str | None = None
    hasta: str | None = None
    dominio: str | None = None


@dataclass
class Documento:
    id: str
    titulo: str
    fecha: str | None
    duracion: str | None
    dominio: str
    descripcion: str | None
    archivo_video: str
    secciones: list[Seccion] = field(default_factory=list)
    segundos_validos: set[int] = field(default_factory=set)

    def temas(self) -> list[Seccion]:
        return [s for s in self.secciones if s.tipo == "tema"]

    def seccion_de_segundo(self, seg: int) -> Seccion | None:
        """Tema cuyo texto menciona ese minuto (o cuyo rango lo contiene)."""
        for s in self.temas():
            if any(a_segundos(t) == seg for t in TS_RE.findall(s.texto)):
                return s
        for s in self.temas():
            if s.desde and s.hasta and a_segundos(s.desde) <= seg <= a_segundos(s.hasta):
                return s
        return None


_TIPO_H2 = {"Resumen": "resumen", "Términos detectados": "terminos", "Reglas y casos especiales detectados": "reglas"}


class Wiki:
    def __init__(self, wiki_dir: Path, asistente_dir: Path):
        self.dir = Path(wiki_dir)
        self.okf = cargar_motor(Path(asistente_dir))
        self.titulo = "Wiki viva"
        self.documentos: dict[str, Documento] = {}
        self.jerga: list[dict] = []
        self.sin_procesar: list[str] = []
        self.cargar()

    # ------------------------------------------------------------- carga
    def cargar(self) -> None:
        okf = self.okf
        idx = self.dir / "index.md"
        if idx.exists():
            fm, _ = okf.leer_frontmatter(idx.read_text(encoding="utf-8"))
            self.titulo = fm.get("title", self.titulo)
        docs = {}
        for ruta, fm, cuerpo in okf.documentos_del_bundle(str(self.dir)):
            did = Path(ruta).stem
            temas = okf.temas_de(cuerpo)
            secciones: list[Seccion] = []
            cur, lineas = None, []

            def cerrar():
                if cur is not None:
                    cur.texto = "\n".join(lineas).strip()

            for linea in cuerpo.splitlines():
                if linea.startswith("## "):
                    cerrar(); lineas = []
                    h2 = linea[3:].strip()
                    cur = Seccion(None, h2, _TIPO_H2[h2], "") if h2 in _TIPO_H2 else None
                    if cur:
                        secciones.append(cur)
                    continue
                m = okf.SECTION_RE.match(linea) if linea.startswith("### ") else None
                if m:
                    cerrar(); lineas = []
                    n = int(m.group(1)) if m.group(1) else None
                    t = temas.get(n, {})
                    cur = Seccion(n, m.group(2), "tema", "", m.group(3) or t.get("desde"), m.group(4) or t.get("hasta"),
                                  t.get("dominio", fm.get("dominio")))
                    secciones.append(cur)
                    continue
                if cur is not None:
                    lineas.append(linea)
            cerrar()
            doc = Documento(did, fm.get("title", did), fm.get("timestamp"), fm.get("duracion"), fm.get("dominio", ""),
                            fm.get("description"), ARCHIVO_VIDEO.get(did, did + ".mp4"), secciones)
            doc.segundos_validos = {a_segundos(t) for s in secciones for t in TS_RE.findall(s.texto)}
            docs[did] = doc
        self.documentos = docs

        self.jerga = []
        glos = self.dir / "_PLANTILLA_Y_GLOSARIO.md"
        if glos.exists():
            for linea in glos.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^\| (.+?) \| (.+?) \| (.*?) \|$", linea)
                if m and '"' in m.group(1) and not linea.startswith("| Lo que dice"):
                    self.jerga.append({"audio": m.group(1), "significado": m.group(2), "nota": m.group(3) or None})
        pend = self.dir / "_grabaciones_sin_procesar.txt"
        self.sin_procesar = [l.strip() for l in pend.read_text(encoding="utf-8").splitlines()
                             if l.strip() and not l.startswith("#")] if pend.exists() else []

    # ------------------------------------------------------------- consultas
    def terminos(self) -> list[dict]:
        out = []
        for d in self.documentos.values():
            for s in d.secciones:
                if s.tipo != "terminos":
                    continue
                for linea in s.texto.splitlines():
                    if not linea.startswith("|") or re.match(r"^\|\s*(Término|-)", linea):
                        continue
                    c = [x.strip() for x in linea.split("|")[1:-1]]
                    if len(c) < 4:
                        continue
                    ts = TS_RE.search(c[3])
                    out.append({"termino": c[0], "variantes_audio": c[1], "significado": c[2], "video_id": d.id,
                                "minuto": hhmmss(ts.group(1)) if ts else None})
        return sorted(out, key=lambda x: normalizar(x["termino"]))

    def buscar(self, pregunta: str, top: int = 10) -> list[dict]:
        """Fragmentos con evidencia. Lista vacía = sin información."""
        res = self.okf.buscar(str(self.dir), pregunta, top=top)
        hits = []
        for r in res.get("resultados", []):
            did = r["archivo"].split("#")[0].rsplit("/", 1)[-1][:-3]
            if did in self.documentos and r.get("timestamp"):
                hits.append({**r, "video_id": did, "segundos": a_segundos(r["timestamp"])})
        return hits

    def contexto(self, hits: list[dict], maximo: int = 6) -> list[tuple[Documento, Seccion]]:
        """Secciones que leen los agentes. Si la mayoría de las coincidencias caen en un mismo
        video, se agregan todos sus temas (la respuesta suele estar repartida en temas contiguos)."""
        vistos, out, por_doc = set(), [], {}
        for h in hits:
            d = self.documentos[h["video_id"]]
            s = next((x for x in d.secciones if x.titulo == h["seccion"]), None)
            if s is None:
                continue
            por_doc.setdefault(d.id, set()).add(s.titulo)
            if (d.id, s.titulo) not in vistos and len(out) < maximo:
                vistos.add((d.id, s.titulo)); out.append((d, s))
        if por_doc:
            top_doc, secs = max(por_doc.items(), key=lambda kv: len(kv[1]))
            if len(secs) >= 3:
                d = self.documentos[top_doc]
                out += [(d, s) for s in d.temas() if (d.id, s.titulo) not in vistos]
        return out

    def minuto_valido(self, video_id: str, ts: str) -> bool:
        d = self.documentos.get(video_id)
        try:
            return bool(d) and a_segundos(ts) in d.segundos_validos
        except (ValueError, AttributeError):
            return False
