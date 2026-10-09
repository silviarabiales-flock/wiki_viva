"""Identidad y roles del usuario.

Fase 2 (desarrollo): el rol llega en el header X-Rol-Dev y el usuario en X-Usuario-Dev.
Fase 5: AUTH_MODO=entra valida el token Bearer de Microsoft Entra ID y toma los roles del token.
"""
import time
from collections import defaultdict, deque
from dataclasses import dataclass

from fastapi import Header, Request

from .errores import ApiError

ROLES = {"lector": 1, "colaborador": 2, "editor": 3}


@dataclass
class Usuario:
    id: str
    rol: str

    def puede(self, rol_minimo: str) -> bool:
        return ROLES[self.rol] >= ROLES[rol_minimo]


def usuario_actual(request: Request,
                   x_rol_dev: str | None = Header(default=None),
                   x_usuario_dev: str | None = Header(default=None)) -> Usuario:
    cfg = request.app.state.config
    if cfg.auth_modo == "desarrollo":
        rol = (x_rol_dev or cfg.rol_dev_por_defecto).strip().lower()
        if rol not in ROLES:
            raise ApiError(401, "no_autorizado", f"Rol de desarrollo desconocido: {rol}.")
        return Usuario(id=(x_usuario_dev or "dev").strip()[:64], rol=rol)
    # TODO fase 5: validar JWT de Entra ID (firma, audiencia, emisor) y mapear roles.
    raise ApiError(503, "servicio_no_disponible", "La autenticación con Microsoft todavía no está configurada.")


def exigir(usuario: Usuario, rol_minimo: str) -> None:
    if not usuario.puede(rol_minimo):
        raise ApiError(403, "sin_permiso", f"Esta acción requiere el rol {rol_minimo}.")


class LimitadorConsultas:
    """Límite simple en memoria: N consultas por minuto por usuario."""

    def __init__(self, por_minuto: int):
        self.por_minuto = por_minuto
        self._hist: dict[str, deque] = defaultdict(deque)

    def verificar(self, usuario_id: str) -> None:
        ahora = time.monotonic()
        h = self._hist[usuario_id]
        while h and ahora - h[0] > 60:
            h.popleft()
        if len(h) >= self.por_minuto:
            raise ApiError(429, "limite_consultas", "Hiciste muchas consultas seguidas. Esperá un minuto y probá de nuevo.")
        h.append(ahora)
