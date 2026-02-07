"""Engagement schemas for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Literal


class ReactionCreate(BaseModel):
    """Schema for adding a reaction to a project"""
    user_id: int = Field(..., description="ID of the user reacting")
    reaction_type: Literal["like", "insightful", "inspiring"] = Field(
        ..., 
        description="Type of reaction"
    )
    weight: float = Field(default=1.0, ge=0.0, le=5.0, description="Reaction weight")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 3,
                "reaction_type": "insightful",
                "weight": 1.0
            }
        }


class ReactionResponse(BaseModel):
    """Schema for reaction creation response"""
    success: bool
    engagement_id: int
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "engagement_id": 42,
                "message": "insightful added"
            }
        }


class EngagementStatsResponse(BaseModel):
    """Schema for project engagement statistics"""
    project_id: int
    total_reactions: int
    likes: int
    insightful: int
    inspiring: int
    impressions: int
    engagement_score: float = Field(..., description="Calculated engagement score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": 5,
                "total_reactions": 45,
                "likes": 20,
                "insightful": 15,
                "inspiring": 10,
                "impressions": 245,
                "engagement_score": 0.32
            }
        }