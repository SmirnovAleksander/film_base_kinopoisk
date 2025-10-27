"""
Base Pydantic schemas for common API responses
"""
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class OperationResponse(BaseModel):
    """Base response for operations (create, update, delete)"""
    status: str = Field(..., description="Operation status")
    message: Optional[str] = Field(None, description="Operation message")
    id: Optional[int] = Field(None, description="ID of affected resource")


class StatusResponse(BaseModel):
    """Simple status response"""
    status: str = Field(..., description="Operation status")


class ListResponse(BaseModel):
    """Base response for list operations"""
    items: list = Field(..., description="List of items")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_count: int = Field(..., description="Total number of items")


class RatingOperationResponse(BaseModel):
    """Response for rating operations"""
    rating: Optional[float] = Field(None, description="User rating")
    created_at: Any = Field(..., description="Creation timestamp")
    updated_at: Any = Field(..., description="Last update timestamp")


class BookmarkOperationResponse(BaseModel):
    """Response for bookmark operations"""
    status: str = Field(..., description="Operation status")
    bookmark_id: Optional[int] = Field(None, description="Bookmark ID if applicable")


class CommentOperationResponse(BaseModel):
    """Response for comment operations"""
    status: str = Field(..., description="Operation status")
    id: Optional[int] = Field(None, description="Comment ID if created")
