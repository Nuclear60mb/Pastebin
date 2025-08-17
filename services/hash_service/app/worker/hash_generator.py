import base64
import uuid
import asyncio
from redis.asyncio import Redis

from app.database.redis_client import get_redis_client


class HashGenerator:
    def __init__(self):
        self.redis: Redis = get_redis_client()
        self.HASH_POOL_KEY = 'hash_pool' 
        self.HASH_POOL_SIZE = 1000 
        self.THRESHOLD = 100 
        
    def generate_hash(self) -> str:
        unique_id = uuid.uuid4()
        b64 = base64.urlsafe_b64encode(unique_id.bytes).decode('utf-8').rstrip('=') 
        return b64[:8]
    
    async def add_hashes_to_pool(self):
        while True:
            current_count = await self.redis.scard(self.HASH_POOL_KEY)

            if current_count < self.HASH_POOL_SIZE:
                new_hashes = {self.generate_hash() for _ in range(self.HASH_POOL_SIZE - current_count)}

                if new_hashes:
                    print(f'trying to add hashes to pool {new_hashes}')
                    await self.redis.sadd(self.HASH_POOL_KEY, *new_hashes)
                    print(f"Added {len(new_hashes)} hashes to the pool.")

            await asyncio.sleep(30)  # Sleep for 30 second before checking again

print('testmsg')

