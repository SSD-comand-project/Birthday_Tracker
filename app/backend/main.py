from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time

from .routers import auth, birthdays, users
from .metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    EXCEPTIONS,
)

app = FastAPI(
    title="Company Birthday Tracker",
    description="A simple internal service to track employee birthdays.",
    version="0.1.0",
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    resp = None
    try:
        resp = await call_next(request)
        return resp
    except Exception:
        EXCEPTIONS.inc()
        raise
    finally:
        elapsed = time.time() - start
        try:
            REQUEST_LATENCY.labels(request.method, request.url.path).observe(elapsed)
        except Exception:
            pass
        try:
            REQUEST_COUNT.labels(
                request.method, request.url.path, str(getattr(resp, "status_code", 500))
            ).inc()
        except Exception:
            pass


@app.get("/metrics", include_in_schema=False)
def metrics():
    """Prometheus metrics endpoint (not shown in OpenAPI)."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
def init_db_on_startup():
    """Initialize database at the start up."""
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
