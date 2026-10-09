"""Interfaz común de los agentes. La simulación (fase 2) y Claude (fase 3) la implementan igual,
así el orquestador, la verificación y la API no cambian al pasar de una a otra."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..motor.wiki import Documento, Seccion


@dataclass
class Afirmacion:
    texto: str
    video_id: str
    minuto: str  # tal como aparece en el documento: m:ss o h:mm:ss
    ficha_id: str | None = None  # ficha consolidada de donde salió, si corresponde


@dataclass
class Sintesis:
    respuesta: str
    vista_funcional: str | None
    vista_tecnica: str | None


Contexto = list[tuple[Documento, Seccion]]


class ProveedorAgentes(Protocol):
    modo: str

    async def reformular(self, pregunta: str, jerga: list[dict]) -> str | None:
        """Reescribe la pregunta con los términos del glosario, o None si no hay nada que corregir."""

    async def funcional(self, pregunta: str, contexto: Contexto, hits: list[dict]) -> list[Afirmacion]:
        """Afirmaciones de negocio respaldadas por la wiki. Lista vacía = sin evidencia."""

    async def tecnico(self, pregunta: str, contexto: Contexto, hits: list[dict]) -> list[Afirmacion]:
        """Afirmaciones técnicas respaldadas por la wiki. Lista vacía = sin evidencia."""

    async def sintesis(self, pregunta: str, citas: list[dict], vista: str) -> Sintesis:
        """Respuesta final que referencia las citas como [F1], [T2]…"""
