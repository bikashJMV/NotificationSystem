from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional, Union

class EventPayload(BaseModel):
    event_name: str
    recipient_email: EmailStr
    cc: Union[EmailStr, list[EmailStr]] = []
    data: Dict[str, Any]
