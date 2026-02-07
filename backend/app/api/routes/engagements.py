"""Engagement endpoints for reactions and statistics."""
from fastapi import APIRouter, HTTPException, Path
from app.api.schema.engagement import (
    ReactionCreate,
    ReactionResponse,
    EngagementStatsResponse
)
from app.repositories.engagements import EngagementRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/projects", tags=["engagements"])


@router.post("/{project_id}/react", response_model=ReactionResponse)
async def add_reaction(
    project_id: int = Path(..., description="ID of the project to react to"),
    reaction: ReactionCreate = None
):
    """
    Add a reaction to a project.
    
    Reactions: like, insightful, inspiring
    Automatically triggers gamification rewards for the reactor.
    """
    try:
        repo = EngagementRepository()
        
        # Create engagement (this already handles reward logic in your existing code)
        engagement_id = repo.create_engagement(
            project_id=project_id,
            user_id=reaction.user_id,
            reaction=reaction.reaction_type,
            weight=reaction.weight
        )
        
        logger.info(f"Reaction added: {reaction.reaction_type} on project {project_id} by user {reaction.user_id}")
        
        return {
            "success": True,
            "engagement_id": engagement_id,
            "message": f"{reaction.reaction_type} added"
        }
        
    except Exception as e:
        logger.error(f"Failed to add reaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}/stats", response_model=EngagementStatsResponse)
async def get_project_stats(
    project_id: int = Path(..., description="ID of the project")
):
    """
    Get engagement statistics for a project.
    
    Returns:
    - Total reactions count
    - Breakdown by reaction type (likes, insightful, inspiring)
    - Impression count
    - Calculated engagement score
    """
    try:
        repo = EngagementRepository()
        
        # Get aggregated stats
        stats = repo.get_project_stats(project_id)
        
        if stats is None:
            # Project might not exist or have no engagements
            logger.warning(f"No stats found for project {project_id}")
            raise HTTPException(status_code=404, detail="Project not found or no engagement data")
        
        logger.info(f"Retrieved stats for project {project_id}")
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get project stats {project_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))