"""Configuración del backend, tomada de variables de entorno."""
import os
from dataclasses import dataclass, field
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[2]


def _lista(valor: str) -> list[str]:
    return [v.strip() for v in valor.split(",") if v.strip()]


@dataclass
class Config:
    wiki_dir: Path = field(default_factory=lambda: Path(os.getenv("WIKI_DIR", RAIZ_REPO / "wiki")))
    asistente_dir: Path = field(default_factory=lambda: Path(os.getenv("ASISTENTE_DIR", RAIZ_REPO / "asistente")))
    db_path: str = field(default_factory=lambda: os.getenv("DB_PATH", str(RAIZ_REPO / "backend" / "wiki_viva.db")))
    # simulacion: agentes deterministas sin API (fase 2). claude: agentes reales (fase 3).
    modo_agentes: str = field(default_factory=lambda: os.getenv("MODO_AGENTES", "simulacion"))
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    modelo_agentes: str = field(default_factory=lambda: os.getenv("MODELO_AGENTES", ""))
    modelo_sintesis: str = field(default_factory=lambda: os.getenv("MODELO_SINTESIS", ""))
    # desarrollo: rol por header X-Rol-Dev. entra: token de Microsoft Entra ID (fase 5).
    auth_modo: str = field(default_factory=lambda: os.getenv("AUTH_MODO", "desarrollo"))
    rol_dev_por_defecto: str = field(default_factory=lambda: os.getenv("ROL_DEV_POR_DEFECTO", "lector"))
    origenes_permitidos: list[str] = field(default_factory=lambda: _lista(os.getenv("ORIGENES_PERMITIDOS", "http://localhost:5173,http://localhost:8080")))
    consultas_por_minuto: int = field(default_factory=lambda: int(os.getenv("CONSULTAS_POR_MINUTO", "20")))
    simulacion_demora_ms: int = field(default_factory=lambda: int(os.getenv("SIMULACION_DEMORA_MS", "0")))


VERSION = "0.3.0"
