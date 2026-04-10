from pydantic import BaseModel, EmailStr
from typing import Any

class EmailRequest(BaseModel):
    recipients: list[EmailStr]
    subject: str
    template: str = "base"
    body: dict[str, Any] = {}

class ApiResponse(BaseModel):
    status_code: int
    prompt_msg: str
    data: Any = None