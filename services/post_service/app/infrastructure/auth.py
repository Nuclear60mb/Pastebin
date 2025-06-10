import os
import httpx
from uuid import UUID
from dotenv import load_dotenv
load_dotenv()


auth_url = os.getenv("VALIDATE_TOKEN_URL")

async def validate_token(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(auth_url, headers=headers)
    return UUID(response.text.strip('"'))
