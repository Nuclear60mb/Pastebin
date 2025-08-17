import asyncio
from app.database.redis_client import get_redis_client

from app.worker.hash_generator import HashGenerator


worker = HashGenerator()



async def check():
    redis = get_redis_client()
    hashes = await redis.smembers("hash_pool")
    print(f"Хэшей в пуле: {len(hashes)}")
    print(list(hashes)[:10])  # первые 10

if __name__ == "__main__":
    asyncio.run(worker.add_hashes_to_pool())
    asyncio.run(check())