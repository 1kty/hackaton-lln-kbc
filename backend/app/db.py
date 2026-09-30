import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "seeder" / "clients.db"


def database_path() -> Path:
    configured = os.environ.get("DATABASE_PATH")
    if configured:
        path = Path(configured)
        return path if path.is_absolute() else PROJECT_ROOT / path
    return DEFAULT_DATABASE_PATH


def connect() -> sqlite3.Connection:
    path = database_path()
    if not path.exists():
        raise FileNotFoundError(f"Customer database not found at {path}")
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection
