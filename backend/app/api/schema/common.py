"""Common schemas used across the API."""
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class StandardResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    message: str
    data: Optional[Any] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    database: str


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    total: int = Field(..., description="Total number of items")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Current offset")
    has_more: bool = Field(..., description="Whether more items exist")