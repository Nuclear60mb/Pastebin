from redis.asyncio import Redis

from app.database.redis_client import get_redis_client


class HashGeneratorService:
    HASH_POOL_KEY = 'hash_pool'
    USED_HASHES_KEY = 'used_hashes'

    def __init__(self):
        self.redis: Redis = get_redis_client()

    async def get_hash(self) -> str | None:
        hash = await self.redis.spop(self.HASH_POOL_KEY)
        await self.redis.sadd(self.USED_HASHES_KEY, hash)
        return hash
    
    async def hashes_count(self) -> int:
        return await self.redis.scard(self.HASH_POOL_KEY)
    
    async def add_hashes_to_pool(self, hash: str):
        return await self.redis.sadd(self.HASH_POOL_KEY, hash) > 0
    
    async def return_hashes_to_pool(self, hash: str):
        await self.redis.srem(self.USED_HASHES_KEY, hash)
        return await self.redis.sadd(self.HASH_POOL_KEY, hash) > 0
    
    