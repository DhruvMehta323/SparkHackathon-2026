"""Feed endpoint for FairRank-based discovery."""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from app.api.schema.feed import FeedResponse, FeedItemResponse
from app.repositories.fairrank import FairRankRepository
from app.repositories.projects import ProjectRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["feed"])


def generate_explanation_badge(project: dict, fairrank_data: dict) -> str:
    """
    Generate explanation badge for why a project is shown in the feed.
    
    Priority order:
    1. Underexposed (impressions < 100)
    2. Fresh (created < 24 hours ago)
    3. High engagement (engagement_score > 0.7)
    4. Default recommendation
    """
    impressions = project.get("impressions", 0)
    created_at = project.get("created_at")
    engagement_score = fairrank_data.get("engagement_score", 0.0)
    
    # Parse created_at timestamp
    try:
        if isinstance(created_at, str):
            created_datetime = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        else:
            created_datetime = created_at
        
        hours_old = (datetime.utcnow() - created_datetime).total_seconds() / 3600
    except Exception as e:
        logger.warning(f"Failed to parse created_at: {e}")
        hours_old = 999  # Default to old
    
    # Generate badge based on priority
    if impressions < 100:
        return "🚀 Boosting emerging project"
    elif hours_old < 24:
        return "✨ Fresh content"
    elif engagement_score > 0.7:
        return "📈 High engagement"
    else:
        return "🎯 Recommended for you"


@router.get("/feed", response_model=FeedResponse)
async def get_discovery_feed(
    limit: int = Query(default=20, ge=1, le=50),
    offset: int = Query(default=0, ge=0)
):
    """
    Get the FairRank-sorted discovery feed.
    
    Projects are ranked by FairRank algorithm which combines:
    - Engagement quality (50%)
    - Underexposed boost (30%)
    - Freshness (20%)
    
    Each project includes an explanation badge showing why it was recommended.
    """
    try:
        fairrank_repo = FairRankRepository()
        
        # Get ranked projects (joins fair_rank_scores with projects)
        ranked_projects = fairrank_repo.get_ranked_feed(limit=limit, offset=offset)
        
        feed_items = []
        for item in ranked_projects:
            project = item["project"]
            fairrank = item["fairrank"]
            
            # Generate explanation badge
            badge = generate_explanation_badge(project, fairrank)
            
            feed_items.append({
                "id": project["id"],
                "title": project["title"],
                "abstract": project["abstract"],
                "creator_id": project["creator_id"],
                "stage": project["stage"],
                "fairrank_score": fairrank["score"],
                "explanation_badge": badge,
                "impressions": project["impressions"],
                "created_at": project["created_at"]
            })
        
        # Get total count
        total = fairrank_repo.count_ranked_projects()
        
        logger.info(f"Feed generated: {len(feed_items)} items (total: {total})")
        
        return {
            "items": feed_items,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate feed: {e}")
        raise HTTPException(status_code=500, detail=str(e))