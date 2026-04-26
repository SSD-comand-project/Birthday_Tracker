from datetime import date, timedelta
from pathlib import Path

from passlib.context import CryptContext

from app.backend.database import get_connection

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "app" / "backend" / "schema.sql"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db() -> None:
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as conn:
        conn.executescript(sql)


def seed_admin_user() -> None:
    admin_hash = pwd_context.hash("admin123")
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO users (username, password_hash, full_name, birth_date)
            VALUES (?, ?, ?, ?)
            """,
            ("admin", admin_hash, "Administrator", "1990-01-01"),
        )
        conn.commit()


def seed_users_every_7_days(year: int | None = None) -> int:
    """
    Create users that have birthdays every 7 days in a year.
    """
    if year is None:
        year = date.today().year

    start = date(year, 1, 1)
    end = date(year, 12, 31)

    password_hash = pwd_context.hash("admin123")
    created = 0
    i = 1
    current = start

    with get_connection() as conn:
        while current <= end:
            username = f"user_{current.strftime('%m%d')}"   # напр. user_0101
            full_name = f"Test User {i}"
            birth_date = current.isoformat()

            conn.execute(
                """
                INSERT OR IGNORE INTO users (username, password_hash, full_name, birth_date)
                VALUES (?, ?, ?, ?)
                """,
                (username, password_hash, full_name, birth_date),
            )

            # rowcount у INSERT OR IGNORE = 1 если вставилось, 0 если пропуск
            if conn.total_changes > created:
                created += 1

            i += 1
            current += timedelta(days=7)

        conn.commit()

    return created


if __name__ == "__main__":
    init_db()
    seed_admin_user()
    inserted = seed_users_every_7_days()
    print("Database initialized")
