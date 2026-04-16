from fastapi import FastAPI

from .routers import auth, birthdays, users

app = FastAPI(
    title="Company Birthday Tracker",
    description="A simple internal service to track employee birthdays.",
    version="0.1.0",
)


@app.on_event("startup")
def init_db_on_startup():
    """Инициализирует базу данных при запуске приложения."""
    from scripts.init_db import init_db, seed_admin_user, seed_users_every_7_days

    init_db()
    seed_admin_user()
    seed_users_every_7_days()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(birthdays.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Birthday Tracker API"}


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "version": "0.1.0"}
