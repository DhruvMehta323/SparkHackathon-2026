"""Admin schemas for system operations and statistics."""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class InitResponse(BaseModel):
    """Schema for database initialization response"""
    success: bool
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Database initialized successfully"
            }
        }


class SeedResponse(BaseModel):
    """Schema for seed data response"""
    success: bool
    message: str
    data: Dict[str, int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Database seeded successfully",
                "data": {
                    "creators": 10,
                    "projects": 20,
                    "engagements": 100,
                    "collab_requests": 5
                }
            }
        }


class PlatformStatsResponse(BaseModel):
    """Schema for platform-wide statistics"""
    total_projects: int
    total_creators: int
    total_engagements: int
    underexposed_projects: int = Field(..., description="Projects with impressions < 100")
    avg_fairrank: float = Field(..., description="Average FairRank score")
    exposure_distribution: Dict[str, int] = Field(..., description="Histogram of impression counts")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_projects": 20,
                "total_creators": 10,
                "total_engagements": 145,
                "underexposed_projects": 8,
                "avg_fairrank": 0.62,
                "exposure_distribution": {
                    "0-50": 5,
                    "51-100": 3,
                    "101-200": 7,
                    "201-500": 4,
                    "500+": 1
                }
            }
        }


class EngineTriggerRequest(BaseModel):
    """Schema for triggering engine calculations"""
    background: bool = Field(default=False, description="Run in background task")
    
    class Config:
        json_schema_extra = {
            "example": {
                "background": False
            }
        }


class EngineTriggerResponse(BaseModel):
    """Schema for engine trigger response"""
    success: bool
    message: str
    job_id: Optional[str] = Field(None, description="Job ID if running in background")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "FairRank calculation completed",
                "job_id": None
            }
        }