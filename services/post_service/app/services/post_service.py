from uuid import UUID

from typing import List

from app.schemas.post_schemas import PostUpdate, PostCreate, PostResponse
from app.repository.post_repository import PostRepository


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def create_post(self, post_data: PostCreate, user_id: UUID) -> PostResponse:
        return await self.repo.create_post(post_data, user_id)

    async def get_post_by_id(self, post_id: UUID) -> PostResponse:
        return await self.repo.get_post_by_id(post_id)

    async def get_all_posts(self, offset: int, limit: int) -> List[PostResponse]:
        return await self.repo.get_all_posts(offset, limit)

    async def get_user_posts(self, user_id: UUID) -> List[PostResponse]:
        return await self.repo.get_user_posts(user_id)

    async def update_post(self, post_id: UUID, post_update: PostUpdate) -> PostResponse:
        return await self.repo.update_post(post_id, post_update)

    async def delete_post(self, post_id: UUID) -> dict:
        return await self.repo.delete_post(post_id)
