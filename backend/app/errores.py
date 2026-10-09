"""Errores de la API con el formato del contrato: {"error": {"codigo", "mensaje"}}."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiError(Exception):
    def __init__(self, status: int, codigo: str, mensaje: str):
        self.status, self.codigo, self.mensaje = status, codigo, mensaje


def cuerpo_error(codigo: str, mensaje: str) -> dict:
    return {"error": {"codigo": codigo, "mensaje": mensaje}}


_CODIGO_POR_STATUS = {400: "consulta_invalida", 401: "no_autorizado", 403: "sin_permiso", 404: "no_encontrado",
                      405: "consulta_invalida", 429: "limite_consultas", 503: "servicio_no_disponible"}


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def _api(_: Request, e: ApiError):
        return JSONResponse(cuerpo_error(e.codigo, e.mensaje), status_code=e.status)

    @app.exception_handler(RequestValidationError)
    async def _validacion(_: Request, e: RequestValidationError):
        detalle = "; ".join(f"{'.'.join(str(x) for x in err['loc'][1:])}: {err['msg']}" for err in e.errors())
        return JSONResponse(cuerpo_error("consulta_invalida", detalle or "Pedido inválido."), status_code=400)

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, e: StarletteHTTPException):
        codigo = _CODIGO_POR_STATUS.get(e.status_code, "error_interno")
        return JSONResponse(cuerpo_error(codigo, str(e.detail)), status_code=e.status_code)

    @app.exception_handler(Exception)
    async def _otro(_: Request, e: Exception):
        return JSONResponse(cuerpo_error("error_interno", "Ocurrió un error inesperado."), status_code=500)
