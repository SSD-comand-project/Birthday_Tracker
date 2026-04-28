import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = os.getenv(
    "DB_PATH",
    str(Path(__file__).resolve().parents[2] / "data" / "birthday_tracker.db"),
)


def get_connection() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
