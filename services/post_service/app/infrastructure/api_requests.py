import httpx
from uuid import UUID

from app.core.config import VALIDATE_TOKEN_URL, HASH_SERVICE_URL


async def validate_token(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(VALIDATE_TOKEN_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        return UUID(data)


async def get_hash():
    async with httpx.AsyncClient() as client:
        response = await client.get(HASH_SERVICE_URL)
        response.raise_for_status()
        return response.json()['hash']