"""Main FastAPI application for CLG Verm\u00f6gensschutz."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, Base, get_session
from app.models import Users, ContentSections, Webhooks, WebhookEvents, Leads, AuditLog, ContactAttempts
from app.routers import health_router, leads_router, admin_router, kpi_router, webhooks_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
      # Initialize database on startup
    logger.info("Initializing database with WAL mode...")
    Base.metadata.create_all(bind=engine)
    
      # Enable WAL mode for all SQLite databases
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL"))
        conn.execute(text("PRAGMA synchronous=NORMAL"))
        conn.execute(text("PRAGMA cache_size=-64000"))
        conn.execute(text("PRAGMA mmap_size=30000000"))
        conn.commit()
    
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="CLG Verm\u00f6gensschutz API",
    description="Backend f\u00fcr CLG Vermögensschutz Landing Page - DACH-kompatibel",
    version="1.0.0",
    lifespan=lifespan,
)


# CORS Middleware (DACH-focused)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(leads_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin")
app.include_router(kpi_router, prefix="/api")
app.include_router(webhooks_router)    # No prefix - directly under /api/webhooks/


# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "CLG Verm\u00f6gensschutz API running", "docs": "/docs"}
