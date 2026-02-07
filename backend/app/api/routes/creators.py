"""Creator endpoints for profile management."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.api.schema.creator import (
    CreatorCreate,
    CreatorUpdate,
    CreatorResponse,
    CreatorListResponse
)
from app.repositories.creators import CreatorRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/creators", tags=["creators"])


@router.post("", response_model=CreatorResponse, status_code=201)
async def create_creator(creator: CreatorCreate):
    """
    Create a new creator profile.
    
    Initializes with level 1 and 0 points (gamification).
    """
    try:
        repo = CreatorRepository()
        
        creator_id = repo.create_creator(
            name=creator.name,
            role=creator.role,
            skills=creator.skills,
            bio=creator.bio,
            location=creator.location,
            availability=creator.availability
        )
        
        logger.info(f"Creator created: ID {creator_id}")
        
        # Return created creator
        result = repo.get_creator(creator_id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to create creator: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=CreatorListResponse)
async def list_creators(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    skills: Optional[str] = Query(
        default=None,
        description="Filter by skills (comma-separated): 'Editing,Color Grading'"
    )
):
    """
    List all creators with pagination.
    
    Optional filtering by skills.
    """
    try:
        repo = CreatorRepository()
        
        # Parse skills filter
        skill_list = skills.split(",") if skills else None
        
        creators = repo.get_all_creators(
            limit=limit,
            offset=offset,
            skill_filter=skill_list
        )
        
        total = repo.count_creators(skill_filter=skill_list)
        
        logger.info(f"Listed {len(creators)} creators (total: {total})")
        
        return {
            "creators": creators,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to list creators: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{creator_id}", response_model=CreatorResponse)
async def get_creator(creator_id: int):
    """
    Get a single creator profile by ID.
    
    Includes gamification data (points, level).
    """
    try:
        repo = CreatorRepository()
        creator = repo.get_creator(creator_id)
        
        if not creator:
            logger.warning(f"Creator not found: ID {creator_id}")
            raise HTTPException(status_code=404, detail="Creator not found")
        
        logger.info(f"Retrieved creator: ID {creator_id}")
        return creator
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get creator {creator_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{creator_id}", response_model=CreatorResponse)
async def update_creator(creator_id: int, update: CreatorUpdate):
    """
    Update a creator profile.
    
    Only provided fields will be updated.
    """
    try:
        repo = CreatorRepository()
        
        # Check if creator exists
        existing = repo.get_creator(creator_id)
        if not existing:
            logger.warning(f"Creator not found for update: ID {creator_id}")
            raise HTTPException(status_code=404, detail="Creator not found")
        
        # Update creator
        repo.update_creator(
            creator_id=creator_id,
            name=update.name,
            role=update.role,
            skills=update.skills,
            bio=update.bio,
            location=update.location,
            availability=update.availability
        )
        
        logger.info(f"Creator updated: ID {creator_id}")
        
        # Return updated creator
        result = repo.get_creator(creator_id)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update creator {creator_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))