"""Creator schemas for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional, List
from app.api.schema.common import PaginationMeta


class CreatorCreate(BaseModel):
    """Schema for creating a new creator profile"""
    name: str = Field(..., min_length=2, max_length=100, description="Creator's name")
    role: str = Field(..., description="Primary role: Director, Editor, Actor, etc.")
    skills: List[str] = Field(..., description="List of skills")
    bio: Optional[str] = Field(None, max_length=1000, description="Creator biography")
    location: Optional[str] = Field(None, description="City or region")
    availability: Optional[str] = Field(None, description="Availability: Weekends, Flexible, etc.")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice Chen",
                "role": "Director",
                "skills": ["Directing", "Cinematography", "Editing"],
                "bio": "Independent filmmaker with 5 years of experience in short films",
                "location": "Chicago",
                "availability": "Weekends"
            }
        }


class CreatorUpdate(BaseModel):
    """Schema for updating a creator profile"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[str] = None
    skills: Optional[List[str]] = None
    bio: Optional[str] = Field(None, max_length=1000)
    location: Optional[str] = None
    availability: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "bio": "Award-winning filmmaker with 7 years of experience",
                "availability": "Flexible"
            }
        }


class CreatorResponse(BaseModel):
    """Schema for creator profile response"""
    id: int
    name: str
    role: str
    skills: List[str]
    bio: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[str] = None
    points: int = 0
    level: int = 1
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Alice Chen",
                "role": "Director",
                "skills": ["Directing", "Cinematography", "Editing"],
                "bio": "Independent filmmaker...",
                "location": "Chicago",
                "availability": "Weekends",
                "points": 150,
                "level": 2,
                "created_at": "2024-01-10T08:00:00"
            }
        }


class CreatorListResponse(BaseModel):
    """Schema for paginated list of creators"""
    creators: List[CreatorResponse]
    pagination: PaginationMeta
    
    class Config:
        json_schema_extra = {
            "example": {
                "creators": [
                    {
                        "id": 1,
                        "name": "Alice Chen",
                        "role": "Director",
                        "skills": ["Directing", "Cinematography"],
                        "location": "Chicago",
                        "points": 150,
                        "level": 2,
                        "created_at": "2024-01-10T08:00:00"
                    }
                ],
                "pagination": {
                    "total": 10,
                    "limit": 10,
                    "offset": 0,
                    "has_more": False
                }
            }
        }