"""Persistencia (SQLite para el piloto; mismo esquema sirve para Postgres)."""
from __future__ import annotations

import json
import re
import sqlite3
import threading
import unicodedata
from datetime import datetime, timezone

ESQUEMA = """
CREATE TABLE IF NOT EXISTS consultas (
  id TEXT PRIMARY KEY, usuario TEXT NOT NULL, pregunta TEXT NOT NULL, vista TEXT NOT NULL,
  sin_informacion INTEGER NOT NULL, resultado TEXT NOT NULL, creada TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS huecos (
  id TEXT PRIMARY KEY, pregunta TEXT NOT NULL, veces INTEGER NOT NULL, estado TEXT NOT NULL,
  creada TEXT NOT NULL, ultima TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS opiniones (
  consulta_id TEXT NOT NULL, usuario TEXT NOT NULL, util INTEGER NOT NULL, comentario TEXT,
  fecha TEXT NOT NULL, PRIMARY KEY (consulta_id, usuario));
CREATE TABLE IF NOT EXISTS links_videos (video_id TEXT PRIMARY KEY, url TEXT NOT NULL);
"""


def ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def id_hueco(pregunta: str) -> str:
    t = unicodedata.normalize("NFD", pregunta.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:120] or "consulta"


class Repositorio:
    def __init__(self, ruta: str):
        self._con = sqlite3.connect(ruta, check_same_thread=False)
        self._con.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        with self._lock:
            self._con.executescript(ESQUEMA)

    def _q(self, sql: str, args=()):
        with self._lock:
            cur = self._con.execute(sql, args)
            self._con.commit()
            return cur.fetchall()

    # consultas
    def guardar_consulta(self, usuario: str, r: dict) -> None:
        self._q("INSERT INTO consultas VALUES (?,?,?,?,?,?,?)",
                (r["consulta_id"], usuario, r["pregunta"], r["vista"], int(r["sin_informacion"]),
                 json.dumps(r, ensure_ascii=False), ahora()))

    def existe_consulta(self, cid: str) -> bool:
        return bool(self._q("SELECT 1 FROM consultas WHERE id=?", (cid,)))

    # huecos
    def registrar_hueco(self, pregunta: str) -> dict:
        hid, t = id_hueco(pregunta), ahora()
        if self._q("SELECT 1 FROM huecos WHERE id=?", (hid,)):
            self._q("UPDATE huecos SET veces=veces+1, ultima=?, estado='abierta' WHERE id=?", (t, hid))
        else:
            self._q("INSERT INTO huecos VALUES (?,?,?,?,?,?)", (hid, pregunta, 1, "abierta", t, t))
        return self.hueco(hid)

    def hueco(self, hid: str) -> dict | None:
        filas = self._q("SELECT * FROM huecos WHERE id=?", (hid,))
        return dict(filas[0]) if filas else None

    def huecos(self, estado: str | None = None) -> list[dict]:
        if estado:
            filas = self._q("SELECT * FROM huecos WHERE estado=? ORDER BY ultima DESC", (estado,))
        else:
            filas = self._q("SELECT * FROM huecos ORDER BY ultima DESC")
        return [dict(f) for f in filas]

    def cambiar_estado_hueco(self, hid: str, estado: str) -> dict | None:
        self._q("UPDATE huecos SET estado=? WHERE id=?", (estado, hid))
        return self.hueco(hid)

    # opiniones
    def guardar_opinion(self, cid: str, usuario: str, util: bool, comentario: str | None) -> None:
        self._q("INSERT OR REPLACE INTO opiniones VALUES (?,?,?,?,?)", (cid, usuario, int(util), comentario, ahora()))

    def opiniones(self, cid: str) -> list[dict]:
        return [dict(f) for f in self._q("SELECT * FROM opiniones WHERE consulta_id=?", (cid,))]

    # links de videos
    def links(self) -> dict[str, str]:
        return {f["video_id"]: f["url"] for f in self._q("SELECT * FROM links_videos")}

    def reemplazar_links(self, links: dict[str, str]) -> dict[str, str]:
        with self._lock:
            self._con.execute("DELETE FROM links_videos")
            self._con.executemany("INSERT INTO links_videos VALUES (?,?)", list(links.items()))
            self._con.commit()
        return self.links()
