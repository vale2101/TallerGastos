from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.auth.jwt_handler import JWTHandler

security = HTTPBearer()

async def has_access(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    try:
        token = credentials.credentials
        payload = JWTHandler().decode_token(token)
        return payload
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
