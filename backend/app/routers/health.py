"""Health check router for Docker healthchecks and monitoring."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas import HealthCheck

router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check(session: Session = Depends(get_session)):
    """Simple health check - used by Docker and load balancers."""
    db_status = "disconnected"
    try:
        session.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        pass
    
       # Check Redis (optional, may fail in local dev)
    cache_status = "unknown"
    try:
        import redis
        r = redis.from_url("redis://clg-redis:6379/0", password="", socket_connect_timeout=1)
        r.ping()
        cache_status = "connected"
    except Exception:
        pass
    
    return HealthCheck(
        status="healthy",
        database=db_status,
        cache=cache_status,
    )
