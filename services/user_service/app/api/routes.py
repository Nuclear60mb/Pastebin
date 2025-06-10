import jwt

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import jwt_settings


security = HTTPBearer()
router = APIRouter()


secret_key = jwt_settings.SECRET_KEY
algorithm = jwt_settings.ALGORITHM


@router.post("/auth/validate_token")
async def validate_token(
    creds: HTTPAuthorizationCredentials = Depends(security),
):
    token = creds.credentials

    try:
        payload = jwt.decode(
            token, secret_key, algorithms=[algorithm], audience="fastapi-users:auth"
        )
        user_id = payload.get('sub')
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
