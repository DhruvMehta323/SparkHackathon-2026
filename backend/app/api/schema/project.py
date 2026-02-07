"""Project schemas for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional, List
from app.api.schema.common import PaginationMeta


class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    title: str = Field(..., min_length=3, max_length=200, description="Project title")
    abstract: str = Field(..., min_length=10, max_length=2000, description="Project description")
    creator_id: int = Field(..., description="ID of the creator")
    stage: str = Field(default="idea", description="Project stage: idea, active, or completed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Urban Dreams",
                "abstract": "A short film exploring life in the modern city through the eyes of diverse characters.",
                "creator_id": 1,
                "stage": "idea"
            }
        }


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    abstract: Optional[str] = Field(None, min_length=10, max_length=2000)
    stage: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Urban Dreams - Updated",
                "stage": "active"
            }
        }


class ProjectResponse(BaseModel):
    """Schema for project response"""
    id: int
    title: str
    abstract: str
    creator_id: int
    stage: str
    created_at: str
    updated_at: Optional[str] = None
    impressions: int = 0
    fairrank_score: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Urban Dreams",
                "abstract": "A short film exploring life in the modern city...",
                "creator_id": 1,
                "stage": "active",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": None,
                "impressions": 245,
                "fairrank_score": 0.78
            }
        }


class SimilarProjectResponse(BaseModel):
    """Schema for similar project in response"""
    id: int
    title: str
    abstract: str
    similarity_score: float = Field(..., description="Similarity score between 0 and 1")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 5,
                "title": "City Lights",
                "abstract": "Documentary about urban nightlife...",
                "similarity_score": 0.85
            }
        }


class ProjectListResponse(BaseModel):
    """Schema for paginated list of projects"""
    projects: List[ProjectResponse]
    pagination: PaginationMeta
    
    class Config:
        json_schema_extra = {
            "example": {
                "projects": [
                    {
                        "id": 1,
                        "title": "Urban Dreams",
                        "abstract": "A short film...",
                        "creator_id": 1,
                        "stage": "active",
                        "created_at": "2024-01-15T10:30:00",
                        "impressions": 245,
                        "fairrank_score": 0.78
                    }
                ],
                "pagination": {
                    "total": 20,
                    "limit": 10,
                    "offset": 0,
                    "has_more": True
                }
            }
        }


class SimilarProjectsResponse(BaseModel):
    """Schema for list of similar projects"""
    similar_projects: List[SimilarProjectResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "similar_projects": [
                    {
                        "id": 5,
                        "title": "City Lights",
                        "abstract": "Documentary...",
                        "similarity_score": 0.85
                    }
                ]
            }
        }