"""Engine trigger endpoints for FairRank and Similarity calculations."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.schema.admin import EngineTriggerRequest, EngineTriggerResponse
from app.services.fairrank_engine import FairRankEngine
from app.services.similarity_engine import SimilarityEngine
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/engines", tags=["engines"])


@router.post("/fairrank", response_model=EngineTriggerResponse)
async def trigger_fairrank(
    request: EngineTriggerRequest = EngineTriggerRequest(),
    background_tasks: BackgroundTasks = None
):
    """
    Trigger FairRank calculation for all projects.
    
    Recalculates:
    - Engagement scores
    - Underexposed boosts
    - Freshness scores
    - Combined FairRank scores
    
    Can run synchronously or in background.
    """
    try:
        engine = FairRankEngine()
        
        if request.background and background_tasks:
            # Run in background
            background_tasks.add_task(engine.run)
            logger.info("FairRank calculation started in background")
            return {
                "success": True,
                "message": "FairRank calculation started in background",
                "job_id": None
            }
        else:
            # Run synchronously
            engine.run()
            logger.info("FairRank calculation completed")
            return {
                "success": True,
                "message": "FairRank calculation completed",
                "job_id": None
            }
            
    except Exception as e:
        logger.error(f"FairRank calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/similarity", response_model=EngineTriggerResponse)
async def trigger_similarity(
    request: EngineTriggerRequest = EngineTriggerRequest(),
    background_tasks: BackgroundTasks = None
):
    """
    Trigger similarity calculation for all projects.
    
    Generates embeddings and computes pairwise similarities.
    This can be a heavy operation for many projects.
    
    Can run synchronously or in background.
    """
    try:
        engine = SimilarityEngine()
        
        if request.background and background_tasks:
            # Run in background
            def run_similarity():
                engine.generate_dummy_embeddings(dim=16)
                engine.compute_all_similarities()
            
            background_tasks.add_task(run_similarity)
            logger.info("Similarity calculation started in background")
            return {
                "success": True,
                "message": "Similarity calculation started in background",
                "job_id": None
            }
        else:
            # Run synchronously
            engine.generate_dummy_embeddings(dim=16)
            engine.compute_all_similarities()
            logger.info("Similarity calculation completed")
            return {
                "success": True,
                "message": "Similarity calculation completed",
                "job_id": None
            }
            
    except Exception as e:
        logger.error(f"Similarity calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))