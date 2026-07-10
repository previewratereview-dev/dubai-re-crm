import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.middleware.error_handler import global_exception_handler, integrity_error_handler
from app.middleware.tools_auth import ToolsAuthMiddleware
from sqlalchemy.exc import IntegrityError

settings = get_settings()

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CRM & AI Calling Platform")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ToolsAuthMiddleware)

# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)

# Routers
from app.routers import auth, leads, customers, appointments, campaigns, calls
from app.routers import notes, users, dashboard, analytics, notifications, ai_agents, tools

app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(customers.router)
app.include_router(appointments.router)
app.include_router(campaigns.router)
app.include_router(calls.router)
app.include_router(notes.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(analytics.router)
app.include_router(notifications.router)
app.include_router(ai_agents.router)
app.include_router(tools.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
