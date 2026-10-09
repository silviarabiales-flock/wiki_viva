"""Agentes con la API de Claude (fase 3, pendiente).

Implementará la misma interfaz que AgentesSimulados usando los prompts de
asistente/SKILL.md: agente funcional y técnico en paralelo (MODELO_AGENTES) y
síntesis con un modelo rápido (MODELO_SINTESIS). La clave ANTHROPIC_API_KEY
vive solo en el servidor.
"""
from ..errores import ApiError


class AgentesClaude:
    modo = "claude"

    def __init__(self, api_key: str, modelo_agentes: str, modelo_sintesis: str):
        if not api_key:
            raise ValueError("MODO_AGENTES=claude requiere ANTHROPIC_API_KEY.")
        self.api_key, self.modelo_agentes, self.modelo_sintesis = api_key, modelo_agentes, modelo_sintesis

    async def _pendiente(self, *_a, **_k):
        raise ApiError(503, "servicio_no_disponible", "Los agentes con Claude se implementan en la fase 3. Usá MODO_AGENTES=simulacion.")

    reformular = funcional = tecnico = sintesis = _pendiente
