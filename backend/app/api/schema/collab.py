"""Collaboration schemas for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional, List


class CollabRequestCreate(BaseModel):
    """Schema for creating a collaboration request"""
    requester_id: int = Field(..., description="ID of the creator making the request")
    project_id: int = Field(..., description="ID of the project needing collaborators")
    role_needed: str = Field(..., description="Role needed: Editor, Cinematographer, etc.")
    skills_needed: List[str] = Field(..., description="List of required skills")
    location_pref: Optional[str] = Field(None, description="Location preference: Chicago, Remote, etc.")
    availability: Optional[str] = Field(None, description="Required availability")
    budget: Optional[str] = Field(default="Revenue share", description="Compensation model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "requester_id": 1,
                "project_id": 5,
                "role_needed": "Editor",
                "skills_needed": ["Final Cut Pro", "Color Grading"],
                "location_pref": "Chicago",
                "availability": "Weekends",
                "budget": "Revenue share"
            }
        }


class CollabRequestResponse(BaseModel):
    """Schema for collaboration request response"""
    id: int
    requester_id: int
    project_id: int
    role_needed: str
    skills_needed: str  # Note: stored as comma-separated string in DB
    location_pref: Optional[str] = None
    availability: Optional[str] = None
    budget: Optional[str] = None
    status: str = "open"
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "requester_id": 1,
                "project_id": 5,
                "role_needed": "Editor",
                "skills_needed": "Final Cut Pro,Color Grading",
                "location_pref": "Chicago",
                "availability": "Weekends",
                "budget": "Revenue share",
                "status": "open",
                "created_at": "2024-01-15T14:30:00"
            }
        }


class CollabMatchResponse(BaseModel):
    """Schema for a single collaboration match"""
    creator_id: int
    creator_name: str
    match_score: float = Field(..., description="Match score between 0 and 1")
    explanation: str = Field(..., description="Explanation of why this match was made")
    skills: List[str]
    location: Optional[str] = None
    availability: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "creator_id": 3,
                "creator_name": "Bob Martinez",
                "match_score": 0.85,
                "explanation": "Has 2/2 required skills • Local collaborator • Available when needed",
                "skills": ["Final Cut Pro", "Color Grading", "Motion Graphics"],
                "location": "Chicago",
                "availability": "Weekends"
            }
        }


class CollabMatchListResponse(BaseModel):
    """Schema for list of collaboration matches"""
    request_id: int
    matches: List[CollabMatchResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": 1,
                "matches": [
                    {
                        "creator_id": 3,
                        "creator_name": "Bob Martinez",
                        "match_score": 0.85,
                        "explanation": "Has 2/2 required skills • Local collaborator",
                        "skills": ["Final Cut Pro", "Color Grading"],
                        "location": "Chicago",
                        "availability": "Weekends"
                    }
                ]
            }
        }