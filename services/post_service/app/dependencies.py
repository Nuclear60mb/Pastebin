from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.post_repository import PostRepository
from app.services.post_service import PostService
from app.database.database import get_db


def get_post_repository(db: AsyncSession = Depends(get_db)):
    return PostRepository(db)


def get_post_service(
        repo: PostRepository = Depends(get_post_repository)
):
    return PostService(repo)
