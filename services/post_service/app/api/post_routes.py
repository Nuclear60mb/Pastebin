from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.post_schemas import (
    PostUpdate,
    PostCreate,
    PostResponse,
    PostResponseWithURL,
    PaginatedPostsResponse,
)
from app.services.post_service import PostService
from app.dependencies import get_post_service
from app.infrastructure.api_requests import validate_token
from app.core.config import BASE_URL


router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=True)


def build_post_response(post) -> PostResponseWithURL:
    return PostResponseWithURL(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        short_url=f"{BASE_URL}/{post.unique_hash}",
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.get("/user_post/{post_id}", response_model=PostResponse)
async def get_post_by_id(
    post_id: UUID, service: PostService = Depends(get_post_service)
):
    return await service.get_post_by_id(post_id)

@router.get("/user_post_hash/{post_hash}", response_model=PostResponse)
async def get_post_by_hash(
    post_hash: str, service: PostService = Depends(get_post_service)
):
    post = await service.get_post_by_hash(post_hash)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/", response_model=PaginatedPostsResponse)
async def get_posts(
    service: PostService = Depends(get_post_service),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items, total = await service.get_all_posts(offset=offset, limit=limit)
    return {
        "items": [PostResponse.model_validate(item) for item in items],
        "limit": limit,
        "offset": offset,
        "total": total,
    }


@router.get("/user_posts", response_model=List[PostResponse])
async def get_user_posts(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: PostService = Depends(get_post_service),
):
    token = creds.credentials
    user_id = await validate_token(token)
    return await service.get_user_posts(user_id)


@router.post("/create_post", response_model=PostResponseWithURL)
async def create_post(
    post_data: PostCreate,
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: PostService = Depends(get_post_service),
):
    token = creds.credentials
    user_id = await validate_token(token)

    post = await service.create_post(post_data, user_id)

    return build_post_response(post)


@router.put("/update_post/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: PostService = Depends(get_post_service),
):
    token = creds.credentials
    user_id = await validate_token(token)

    post = await service.get_post_by_id(post_id)

    if user_id != post.author_id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this post"
        )

    return await service.update_post(post_id, post_update)


@router.delete("/delete_post/{post_id}")
async def delete_post(
    post_id: UUID,
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: PostService = Depends(get_post_service),
):
    token = creds.credentials
    user_id = await validate_token(token)

    post = await service.get_post_by_id(post_id)
    if user_id != post.author_id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this post"
        )

    await service.delete_post(post_id=post_id)
    return {"message": "Post has been deletedd"}
