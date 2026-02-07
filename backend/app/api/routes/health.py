"""Health check endpoint."""
from fastapi import APIRouter
from app.api.schema.common import HealthResponse
from app.core.database import get_connection
from datetime import datetime
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the API status and database connectivity status.
    """
    # Test database connection
    try:
        conn = get_connection()
        conn.close()
        db_status = "connected"
        logger.info("Health check: database connected")
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Health check: database error - {e}")
    
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status
    }