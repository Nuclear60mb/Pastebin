import uuid

from fastapi_users import schemas
from typing import Optional
from datetime import date
from pydantic import EmailStr


class UserCreate(schemas.BaseUserCreate):
    username: str
    gender: str


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: Optional[str] = None
    user_bio: Optional[str] = None
    live: Optional[str] = None
    posts_count: Optional[int] = 0
    gender: Optional[str] = None
    birthday: Optional[date] = None


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    user_bio: Optional[str] = None
    live: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
