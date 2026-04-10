from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional, Union

class EventPayload(BaseModel):
    event_name: str
    recipient_email: EmailStr
    cc: Optional[Union[EmailStr, list[EmailStr]]] = None
    data: Dict[str, Any]
