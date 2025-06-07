from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.schemas.post_schemas import PostUpdate, PostCreate, PostResponse, PaginatedPostsResponse
from app.services.post_service import PostService
from app.infrastructure.auth import get_user_id_from_token
from app.dependencies import get_post_service

router = APIRouter()


@router.get('/user_post/{post_id}', response_model=PostResponse)
async def get_user_post(post_id: UUID, service: PostService = Depends(get_post_service)):
    return await service.get_post_by_id(post_id)


@router.get('/', response_model=PaginatedPostsResponse)
async def get_posts(
        service: PostService = Depends(get_post_service),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0)):
    items, total = await service.get_all_posts(offset=offset, limit=limit)
    return {
        'items': [PostResponse.model_validate(item) for item in items],
        'limit': limit,
        'offset': offset,
        'total': total
    }


@router.get('/user_posts', response_model=List[PostResponse])
async def get_user_posts(
    user_id: UUID = Depends(get_user_id_from_token),
    service: PostService = Depends(get_post_service),
):
    return await service.get_user_posts(user_id)


@router.post('/create_post', response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    user_id: UUID = Depends(get_user_id_from_token),
    service: PostService = Depends(get_post_service)
):

    return await service.create_post(
        post_data=post_data,
        user_id=user_id
    )


@router.put('/update_post/{post_id}', response_model=PostResponse)
async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    user_id: UUID = Depends(get_user_id_from_token),
    service: PostService = Depends(get_post_service)
):
    post = await service.get_post_by_id(post_id)

    if user_id != post.author_id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this post")
    
    return await service.update_post(
        post_id=post_id,
        post_update=post_update
    )

@router.delete('/delete_post/{post_id}')
async def delete_post(
    post_id: UUID,
    user_id: UUID = Depends(get_user_id_from_token),
    service: PostService = Depends(get_post_service)
):
    post = await service.get_post_by_id(post_id)
    if user_id != post.author_id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this post")

    await service.delete_post(post_id=post_id)
    return {'message': 'Post has been deleted'}
