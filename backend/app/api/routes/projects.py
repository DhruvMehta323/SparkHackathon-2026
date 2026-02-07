"""Project endpoints for CRUD operations and similarity."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.api.schema.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
    SimilarProjectsResponse
)
from app.repositories.projects import ProjectRepository
from app.repositories.similarity import SimilarityRepository
from app.services.similarity_engine import SimilarityEngine
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate):
    """
    Create a new project.
    
    Automatically generates text embeddings for similarity detection.
    """
    try:
        repo = ProjectRepository()
        
        # Create project in database
        project_id = repo.create_project(
            title=project.title,
            abstract=project.abstract,
            creator_id=project.creator_id,
            stage=project.stage
        )
        
        logger.info(f"Project created: ID {project_id}")
        
        # Generate embedding for similarity detection
        try:
            engine = SimilarityEngine()
            engine.generate_embedding_for_project(project_id)
            logger.info(f"Embedding generated for project {project_id}")
        except Exception as e:
            logger.warning(f"Failed to generate embedding for project {project_id}: {e}")
            # Don't fail the request if embedding generation fails
        
        # Return created project
        result = repo.get_project(project_id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    stage: Optional[str] = Query(default=None, description="Filter by stage: idea, active, or completed")
):
    """
    List all projects with pagination.
    
    Optional filtering by project stage.
    """
    try:
        repo = ProjectRepository()
        
        projects = repo.get_all_projects(
            limit=limit,
            offset=offset,
            stage_filter=stage
        )
        
        total = repo.count_projects(stage_filter=stage)
        
        logger.info(f"Listed {len(projects)} projects (total: {total})")
        
        return {
            "projects": projects,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """
    Get a single project by ID.
    
    Includes FairRank score if available.
    """
    try:
        repo = ProjectRepository()
        project = repo.get_project(project_id)
        
        if not project:
            logger.warning(f"Project not found: ID {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        
        logger.info(f"Retrieved project: ID {project_id}")
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, update: ProjectUpdate):
    """
    Update a project.
    
    Only provided fields will be updated.
    Re-generates embeddings if title or abstract changed.
    """
    try:
        repo = ProjectRepository()
        
        # Check if project exists
        existing = repo.get_project(project_id)
        if not existing:
            logger.warning(f"Project not found for update: ID {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Update project
        repo.update_project(
            project_id=project_id,
            title=update.title,
            abstract=update.abstract,
            stage=update.stage
        )
        
        logger.info(f"Project updated: ID {project_id}")
        
        # Re-generate embedding if text changed
        if update.title or update.abstract:
            try:
                engine = SimilarityEngine()
                engine.generate_embedding_for_project(project_id)
                logger.info(f"Embedding regenerated for project {project_id}")
            except Exception as e:
                logger.warning(f"Failed to regenerate embedding: {e}")
        
        # Return updated project
        result = repo.get_project(project_id)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}/similar", response_model=SimilarProjectsResponse)
async def get_similar_projects(
    project_id: int,
    limit: int = Query(default=3, ge=1, le=10)
):
    """
    Get similar projects based on text embeddings.
    
    Uses cosine similarity to find semantically related projects.
    """
    try:
        repo = SimilarityRepository()
        
        # Check if project exists
        from app.repositories.projects import ProjectRepository
        project_repo = ProjectRepository()
        project = project_repo.get_project(project_id)
        
        if not project:
            logger.warning(f"Project not found for similarity: ID {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get similar projects
        similar = repo.get_similar_projects(project_id, limit=limit)
        
        logger.info(f"Found {len(similar)} similar projects for ID {project_id}")
        
        return {
            "similar_projects": similar
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get similar projects for {project_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))