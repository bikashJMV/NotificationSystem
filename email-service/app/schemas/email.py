from pydantic import BaseModel, EmailStr
from typing import Dict, Any

class EventPayload(BaseModel):
    event_name: str
    recipient_email: EmailStr
    data: Dict[str, Any]
