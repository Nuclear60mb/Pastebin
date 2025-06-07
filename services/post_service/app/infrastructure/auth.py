import os

from jose import jwt
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from datetime import datetime
from uuid import UUID


load_dotenv()

secret_key = os.getenv("JWT_SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


def get_user_id_from_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])

    user_id = payload.get("user_id")
    exp = payload.get("exp")

    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found")
    if exp and datetime.fromtimestamp(exp) < datetime.now():
        raise HTTPException(status_code=401, detail="Token has expired")
    
    return UUID(user_id)