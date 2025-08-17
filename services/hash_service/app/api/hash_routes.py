from fastapi import APIRouter, HTTPException

from app.services.hash_generator_service import HashGeneratorService


router = APIRouter()
hash_service = HashGeneratorService()


@router.get('/hash')
async def get_hash():
    hash = await hash_service.get_hash()
    if not hash:
        raise HTTPException(status_code=404, detail="No hashes available")
    
    return {"hash": hash}

@router.get('/hash/count')
async def get_hash_count():
    count = await hash_service.hashes_count()
    return {"count": count}

@router.post('/hash')
async def add_hash(hash: str):
    added = await hash_service.add_hashes_to_pool(hash)
    if not added:
        return {'added': False, 'message': 'hash already exists'}
    return {'added': True, 'message': 'hash added successfully'}

@router.post('/hash/return')
async def return_hash(hash: str):
    await hash_service.return_hashes_to_pool(hash)
    return {'message': 'hash returned to pool successfully'}