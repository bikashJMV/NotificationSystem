from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from bcrypt import checkpw, gensalt, hashpw
from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify X-API-Key against bcrypt hash stored in env"""
    if not checkpw(api_key.encode(), settings.EMAIL_SERVICE_API_KEY_HASH.encode()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key

def hash_api_key(api_key: str) -> str:
    """Utility: generate bcrypt hash for a new API key"""
    return hashpw(api_key.encode(), gensalt(rounds=settings.BCRYPT_ROUNDS)).decode()
