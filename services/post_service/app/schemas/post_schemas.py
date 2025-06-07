from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    author_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedPostsResponse(BaseModel):
    items: list[PostResponse]
    limit: int
    offset: int
    total: int

    model_config = ConfigDict(from_attributes=True)
