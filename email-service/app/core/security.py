# app/core/security.py
import hmac
import hashlib
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    incoming = hashlib.sha256(api_key.encode()).hexdigest()
    if not hmac.compare_digest(incoming, settings.EMAIL_SERVICE_API_KEY_HASH):
        raise HTTPException(status_code=403, detail="Invalid API key")