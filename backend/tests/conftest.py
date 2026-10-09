from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.jsonschema import DRAFT202012

from app.config import Config
from app.main import crear_app

RAIZ = Path(__file__).resolve().parents[2]


@pytest.fixture()
def cliente(tmp_path):
    cfg = Config()
    cfg.db_path = str(tmp_path / "test.db")
    cfg.modo_agentes = "simulacion"
    cfg.auth_modo = "desarrollo"
    cfg.consultas_por_minuto = 1000
    return TestClient(crear_app(cfg))


@pytest.fixture(scope="session")
def contrato():
    """Valida un cuerpo contra un esquema de docs/api/openapi.yaml."""
    spec = yaml.safe_load((RAIZ / "docs" / "api" / "openapi.yaml").read_text(encoding="utf-8"))
    registro = Registry().with_resource("urn:contrato", DRAFT202012.create_resource(spec))

    def validar(nombre: str, cuerpo):
        esquema = {"$ref": f"urn:contrato#/components/schemas/{nombre}"}
        Draft202012Validator(esquema, registry=registro).validate(cuerpo)
        return cuerpo

    return validar


ROL = lambda r, u="ana": {"X-Rol-Dev": r, "X-Usuario-Dev": u}  # noqa: E731
