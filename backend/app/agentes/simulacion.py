"""Agentes simulados (fase 2): deterministas, sin API ni costo.

Arman las afirmaciones con el texto literal de los fragmentos encontrados, así se puede
probar la comunicación completa frontend ↔ backend y la verificación de minutos.
"""
from __future__ import annotations

import asyncio
import re

from .base import Afirmacion, Contexto, Sintesis

_FUNCIONAL = {"funcional", "ambos"}
_TECNICO = {"tecnico", "ambos"}
_LISTAS = {"Términos detectados", "Reglas y casos especiales detectados"}


def limpiar(texto: str, maximo: int = 320) -> str:
    t = texto.strip()
    if t.startswith("|"):
        filas = [l for l in t.splitlines() if l.startswith("|") and not re.match(r"^\|\s*-", l)]
        if len(filas) == 1:  # fila suelta de la tabla de términos: "término: significado"
            c = [x.strip() for x in filas[0].split("|")[1:-1]]
            t = f"{c[0]}: {c[2]}" if len(c) >= 3 else filas[0]
        else:  # tabla completa: se descarta el encabezado y se resume cada fila
            filas = filas[1:]
            t = "; ".join(" → ".join(x.strip() for x in f.split("|")[1:-1]) for f in filas) + "."
    t = re.sub(r"\s*\[[^\]]*·\s*\d{1,2}:\d{2}(?::\d{2})?\]\([^)]*\)", "", t)  # citas de fichas
    t = re.sub(r"\[([^\]]+)\]\([^)]*\.md[^)]*\)", r"\1", t)  # links a otras fichas
    t = re.sub(r"^>\s*", "", t)
    t = re.sub(r"^-\s*", "", t)
    t = re.sub(r"\[\d{1,2}:\d{2}(?::\d{2})?(?:[–-]\d{1,2}:\d{2}(?::\d{2})?)?\]\s*", "", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > maximo:
        corte = t.rfind(". ", 0, maximo)
        t = t[: corte + 1] if corte > 80 else t[:maximo].rstrip() + "…"
    return t


class AgentesSimulados:
    modo = "simulacion"

    def __init__(self, demora_ms: int = 0):
        self.demora = demora_ms / 1000

    async def _pausa(self):
        if self.demora:
            await asyncio.sleep(self.demora)

    def _elegir(self, hits: list[dict], dominios: set[str], maximo: int = 4) -> list[Afirmacion]:
        out, vistos = [], set()
        for h in sorted(hits, key=lambda x: -x["puntaje"]):
            if h["dominio"] not in dominios and h["seccion"] not in _LISTAS:
                continue
            texto = limpiar(h["texto"])
            if not texto or texto in vistos:
                continue
            vistos.add(texto)
            # el minuto se toma del propio fragmento (como lo haría un agente que lee el texto)
            m = re.search(r"\[(\d{1,2}:\d{2}(?::\d{2})?)", h["texto"]) or re.search(r"(\d{1,2}:\d{2}(?::\d{2})?)\s*\|?\s*$", h["texto"])
            minuto = m.group(1) if m else h["timestamp"]
            if h.get("ficha_id"):
                minuto = h["timestamp"]  # en fichas, el minuto es el de la primera cita del fragmento
            out.append(Afirmacion(texto, h["video_id"], minuto, h.get("ficha_id")))
            if len(out) >= maximo:
                break
        return out

    async def reformular(self, pregunta: str, jerga: list[dict]) -> str | None:
        await self._pausa()
        p = pregunta
        for j in jerga:
            for variante in re.findall(r'"([^"]+)"', j["audio"]):
                if variante and re.search(rf"\b{re.escape(variante)}\b", p, re.I):
                    p = re.sub(rf"\b{re.escape(variante)}\b", re.sub(r"[*`]", "", j["significado"]).split("(")[0].strip(), p, flags=re.I)
        return p if p != pregunta else None

    async def funcional(self, pregunta: str, contexto: Contexto, hits: list[dict]) -> list[Afirmacion]:
        await self._pausa()
        return self._elegir(hits, _FUNCIONAL)

    async def tecnico(self, pregunta: str, contexto: Contexto, hits: list[dict]) -> list[Afirmacion]:
        await self._pausa()
        return self._elegir(hits, _TECNICO)

    async def sintesis(self, pregunta: str, citas: list[dict], vista: str) -> Sintesis:
        await self._pausa()
        orden, vistos = [], set()
        for c in citas:  # sin repetir la misma afirmación de los dos agentes
            if c["texto"] not in vistos:
                vistos.add(c["texto"]); orden.append(c)
        orden = orden[:5]
        pasos = "\n".join(f"{i}. {c['texto']} [{c['id']}]" for i, c in enumerate(orden, 1))
        f = next((c for c in citas if c["agente"] == "funcional"), None)
        t = next((c for c in citas if c["agente"] == "tecnico"), None)
        return Sintesis(
            respuesta="Según la wiki (respuesta simulada, sin IA):\n" + pasos,
            vista_funcional=f"{f['texto']} [{f['id']}]" if f and vista != "tecnica" else None,
            vista_tecnica=f"{t['texto']} [{t['id']}]" if t and vista != "funcional" else None,
        )
