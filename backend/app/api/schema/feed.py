"""Feed schemas for discovery feed responses."""
from pydantic import BaseModel, Field
from typing import List
from app.api.schema.common import PaginationMeta


class FeedItemResponse(BaseModel):
    """Schema for a single item in the discovery feed"""
    id: int
    title: str
    abstract: str
    creator_id: int
    stage: str
    fairrank_score: float = Field(..., description="FairRank score for this project")
    explanation_badge: str = Field(..., description="Explanation for why this is shown")
    impressions: int
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 5,
                "title": "Urban Dreams",
                "abstract": "A short film exploring city life...",
                "creator_id": 1,
                "stage": "active",
                "fairrank_score": 0.78,
                "explanation_badge": "🚀 Boosting emerging project",
                "impressions": 45,
                "created_at": "2024-01-15T10:30:00"
            }
        }


class FeedResponse(BaseModel):
    """Schema for the full discovery feed"""
    items: List[FeedItemResponse]
    pagination: PaginationMeta
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 5,
                        "title": "Urban Dreams",
                        "abstract": "A short film...",
                        "creator_id": 1,
                        "stage": "active",
                        "fairrank_score": 0.78,
                        "explanation_badge": "🚀 Boosting emerging project",
                        "impressions": 45,
                        "created_at": "2024-01-15T10:30:00"
                    },
                    {
                        "id": 12,
                        "title": "City Lights",
                        "abstract": "Documentary about...",
                        "creator_id": 3,
                        "stage": "idea",
                        "fairrank_score": 0.65,
                        "explanation_badge": "✨ Fresh content",
                        "impressions": 12,
                        "created_at": "2024-02-06T18:00:00"
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