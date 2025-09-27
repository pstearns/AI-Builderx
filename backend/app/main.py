from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from .core.settings import get_settings
from .core.logging import (
    log_request, 
    http_exception_handler, 
    validation_exception_handler, 
    general_exception_handler
)
from .db.database import connect_to_mongo, close_mongo_connection, get_database
from .db.repositories.user_repository import UserRepository
from .db.repositories.task_repository import TaskRepository
from .db.repositories.label_repository import LabelRepository
from .api import auth, tasks, labels

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    
    # Create database indexes
    db = get_database()
    user_repo = UserRepository(db)
    task_repo = TaskRepository(db)
    label_repo = LabelRepository(db)
    
    await user_repo.create_indexes()
    await task_repo.create_indexes()
    await label_repo.create_indexes()
    
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "auth", "description": "Authentication routes"},
        {"name": "users", "description": "User profile routes"},
        {"name": "tasks", "description": "Task CRUD routes"},
        {"name": "labels", "description": "Label CRUD routes"},
    ],
)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(labels.router)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all requests"""
    response = await call_next(request)
    log_request(request, response)
    return response

@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
