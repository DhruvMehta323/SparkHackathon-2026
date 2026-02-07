"""Admin endpoints for database management and statistics."""
from fastapi import APIRouter, HTTPException
from app.api.schema.admin import InitResponse, SeedResponse, PlatformStatsResponse
from app.api.schema.common import StandardResponse
from app.scripts.init_db import init_database
from app.repositories.platform_stats import PlatformStatsRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/init", response_model=InitResponse)
async def initialize_database():
    """
    Initialize database schema.
    
    Creates all necessary tables. This operation is idempotent.
    """
    try:
        init_database()
        logger.info("Database initialized successfully")
        return {
            "success": True,
            "message": "Database initialized successfully"
        }
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/seed", response_model=SeedResponse)
async def seed_database():
    """
    Seed database with demo data.
    
    Creates sample projects, creators, engagements, and collaboration requests.
    """
    try:
        # Import here to avoid circular imports
        from app.scripts.seed_data import seed_database as seed_func
        
        result = seed_func()
        logger.info(f"Database seeded: {result}")
        
        return {
            "success": True,
            "message": "Database seeded successfully",
            "data": result
        }
    except ImportError:
        logger.error("Seed script not found")
        raise HTTPException(
            status_code=501,
            detail="Seed script not yet implemented. Create app/scripts/seed_data.py"
        )
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=PlatformStatsResponse)
async def get_platform_statistics():
    """
    Get platform-wide statistics.
    
    Returns metrics including:
    - Total projects, creators, engagements
    - Underexposed projects count
    - Average FairRank score
    - Exposure distribution histogram
    """
    try:
        repo = PlatformStatsRepository()
        
        total_projects = repo.count_projects()
        total_creators = repo.count_creators()
        total_engagements = repo.count_engagements()
        underexposed = repo.count_underexposed_projects(threshold=100)
        avg_fairrank = repo.get_avg_fairrank()
        distribution = repo.get_exposure_distribution()
        
        logger.info("Platform statistics retrieved")
        
        return {
            "total_projects": total_projects,
            "total_creators": total_creators,
            "total_engagements": total_engagements,
            "underexposed_projects": underexposed,
            "avg_fairrank": avg_fairrank,
            "exposure_distribution": distribution
        }
    except Exception as e:
        logger.error(f"Failed to get platform stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))