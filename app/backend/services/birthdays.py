from datetime import date, timedelta
from app.backend.database import get_db


def get_birthdays_today() -> list[dict]:
    today_md = date.today().strftime("%m-%d")
    query = """
    SELECT id, username, full_name, birth_date
    FROM users
    WHERE strftime('%m-%d', birth_date) = ?
    ORDER BY full_name
    """
    with get_db() as conn:
        rows = conn.execute(query, (today_md,)).fetchall()
        return [dict(r) for r in rows]


def get_birthdays_next_7_days() -> list[dict]:
    days = [(date.today() + timedelta(days=i)).strftime("%m-%d") for i in range(1, 8)]

    query = """
    SELECT id, username, full_name, birth_date
    FROM users
    WHERE strftime('%m-%d', birth_date) IN (?, ?, ?, ?, ?, ?, ?)
    ORDER BY strftime('%m-%d', birth_date), full_name
    """

    with get_db() as conn:
        rows = conn.execute(query, tuple(days)).fetchall()
        return [dict(r) for r in rows]
