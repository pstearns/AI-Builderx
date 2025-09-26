from fastapi import FastAPI
from .core.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "auth", "description": "Authentication routes (to be implemented)"},
        {"name": "users", "description": "User profile routes (to be implemented)"},
        {"name": "tasks", "description": "Task CRUD routes (to be implemented)"},
        {"name": "labels", "description": "Label CRUD routes (to be implemented)"},
    ],
)

@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
