from uuid import UUID
from fastapi import HTTPException, status

from typing import List
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.post_schemas import PostResponse, PostUpdate, PostCreate
from app.database.models import Post
from app.infrastructure.api_requests import get_hash


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_post_by_id(self, post_id: UUID) -> Post:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    
    async def get_post_by_hash(self, post_hash: str) -> Post|None:
        result = await self.db.execute(select(Post).where(Post.unique_hash == post_hash))
        post = result.scalars().first()



    async def get_all_posts(self, offset: int, limit: int) -> List[Post]:
        stmt = select(Post).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        total = await self.db.scalar(select(func.count()).select_from(Post))
        return items, total

    async def get_user_posts(self, user_id: UUID) -> List[Post]:

        result = await self.db.execute(select(Post).where(Post.author_id == user_id))
        posts = result.scalars().all()
        return [PostResponse.model_validate(post) for post in posts]

    async def create_post(self, post: PostCreate, user_id: UUID) -> Post:
        hash_value = await get_hash()
        new_post = Post(**post.model_dump(), author_id=user_id, unique_hash=hash_value)

        try:
            self.db.add(new_post)
            await self.db.commit()
            print(f"DEBUG after commit: new_post.id={new_post.id}")
            await self.db.refresh(new_post)
        except Exception as e:
            print(f"Error creating post: {e}")
            await self.db.rollback()
            raise e

        return new_post

    async def update_post(self, post_id: UUID, post_update: PostUpdate) -> Post:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()

        for key, value in post_update.model_dump(exclude_unset=True).items():
            setattr(post, key, value)

        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def delete_post(self, post_id: UUID) -> dict:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()

        await self.db.delete(post)
        await self.db.commit()

        return {"message": "Post has been deleted"}
