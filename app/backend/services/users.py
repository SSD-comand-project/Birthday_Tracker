from typing import Any, Optional

from passlib.context import CryptContext

from app.backend.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _to_dict(row) -> dict[str, Any]:
    return dict(row) if row else None


def create_user(username: str, password_hash: str, full_name: str, birth_date: str) -> int:
    query = """
    INSERT INTO users (username, password_hash, full_name, birth_date)
    VALUES (?, ?, ?, ?)
    """
    with get_db() as conn:
        cur = conn.execute(query, (username, password_hash, full_name, birth_date))
        return cur.lastrowid


def register_user(username: str, password: str, full_name: str, birth_date: str) -> int:
    password_hash = pwd_context.hash(password)
    return create_user(username, password_hash, full_name, birth_date)


def get_user_by_username(username: str) -> Optional[dict[str, Any]]:
    query = "SELECT * FROM users WHERE username = ?"
    with get_db() as conn:
        row = conn.execute(query, (username,)).fetchone()
        return _to_dict(row)


def get_user_by_id(user_id: int) -> Optional[dict[str, Any]]:
    query = "SELECT * FROM users WHERE id = ?"
    with get_db() as conn:
        row = conn.execute(query, (user_id,)).fetchone()
        return _to_dict(row)


def authenticate_user(username: str, password: str) -> Optional[dict[str, Any]]:
    user = get_user_by_username(username)
    if not user:
        return None
    if not pwd_context.verify(password, user["password_hash"]):
        return None
    return user


def list_users() -> list[dict[str, Any]]:
    query = "SELECT * FROM users ORDER BY full_name ASC"
    with get_db() as conn:
        rows = conn.execute(query).fetchall()
        return [dict(r) for r in rows]


def update_user_profile(user_id: int, full_name: str, birth_date: str) -> bool:
    query = """
    UPDATE users
    SET full_name = ?, birth_date = ?
    WHERE id = ?
    """
    with get_db() as conn:
        cur = conn.execute(query, (full_name, birth_date, user_id))
        return cur.rowcount > 0


def delete_user(user_id: int) -> bool:
    query = "DELETE FROM users WHERE id = ?"
    with get_db() as conn:
        cur = conn.execute(query, (user_id,))
        return cur.rowcount > 0
