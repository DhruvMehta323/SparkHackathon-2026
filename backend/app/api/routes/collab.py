"""Collaboration endpoints for requests and matching."""
from fastapi import APIRouter, HTTPException, Path
from app.api.schema.collab import (
    CollabRequestCreate,
    CollabRequestResponse,
    CollabMatchListResponse
)
from app.repositories.collab import CollabRepository
from app.services.matching_engine import MatchingEngine
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/collab", tags=["collaboration"])


@router.post("/requests", response_model=CollabRequestResponse, status_code=201)
async def create_collab_request(request: CollabRequestCreate):
    """
    Create a collaboration request.
    
    Specifies what role and skills are needed for a project.
    Can include location preferences and availability requirements.
    """
    try:
        repo = CollabRepository()
        
        # Convert skills list to comma-separated string for storage
        skills_str = ",".join(request.skills_needed)
        
        request_id = repo.create_request(
            requester_id=request.requester_id,
            project_id=request.project_id,
            role_needed=request.role_needed,
            skills_needed=skills_str,
            location_pref=request.location_pref,
            availability=request.availability,
            budget=request.budget
        )
        
        logger.info(f"Collaboration request created: ID {request_id}")
        
        # Return created request
        result = repo.get_request(request_id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to create collaboration request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/requests/{request_id}", response_model=CollabRequestResponse)
async def get_collab_request(
    request_id: int = Path(..., description="ID of the collaboration request")
):
    """
    Get a collaboration request by ID.
    
    Returns the request details including required role, skills, and preferences.
    """
    try:
        repo = CollabRepository()
        request = repo.get_request(request_id)
        
        if not request:
            logger.warning(f"Collaboration request not found: ID {request_id}")
            raise HTTPException(status_code=404, detail="Collaboration request not found")
        
        logger.info(f"Retrieved collaboration request: ID {request_id}")
        return request
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get collaboration request {request_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/requests/{request_id}/matches", response_model=CollabMatchListResponse)
async def get_collab_matches(
    request_id: int = Path(..., description="ID of the collaboration request")
):
    """
    Get matched creators for a collaboration request.
    
    Runs the matching engine which scores creators based on:
    - Skill overlap with requirements (60%)
    - Location proximity (20%)
    - Availability match (20%)
    
    Returns top matches with explanations.
    """
    try:
        # Check if request exists
        repo = CollabRepository()
        request = repo.get_request(request_id)
        
        if not request:
            logger.warning(f"Collaboration request not found for matching: ID {request_id}")
            raise HTTPException(status_code=404, detail="Collaboration request not found")
        
        # Run matching engine (this writes results to collab_matches table)
        engine = MatchingEngine()
        engine.run(request_id)
        
        logger.info(f"Matching engine completed for request {request_id}")
        
        # Get matches from database
        matches = repo.get_matches_for_request(request_id)
        
        logger.info(f"Found {len(matches)} matches for request {request_id}")
        
        return {
            "request_id": request_id,
            "matches": matches
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get matches for request {request_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))