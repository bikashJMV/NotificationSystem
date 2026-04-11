from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Any, Optional
from enum import Enum

class RoleEnum(str, Enum):
    IT_OPS = "it_ops"
    ADMIN = "admin"
    EMPLOYEE = "employee"

class EventEnum(str, Enum):
    ASSET_ASSIGNED = "asset.assigned"
    ASSET_RETURNED = "asset.returned"
    FORCE_RECALL_OLD = "force.recall.old"
    FORCE_RECALL_NEW = "force.recall.new"

class AssetData(BaseModel):
    category: str = Field(..., description="Asset Category: Laptop/Desktop/etc")
    model_no: str = Field(..., description="Model Number")
    asset_id: str = Field(..., description="Asset ID/Tag")

    @field_validator('category', 'model_no', 'asset_id')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

class RecipientInfo(BaseModel):
    email: EmailStr
    name: str
    role: RoleEnum

class EmailRequest(BaseModel):
    event_name: EventEnum
    primary_recipient: RecipientInfo
    admin_email: EmailStr
    admin_name: str
    all_admin_emails: List[EmailStr] = []
    asset_data: AssetData
    previous_employee_email: Optional[EmailStr] = None
    new_employee_email: Optional[EmailStr] = None

class ApiResponse(BaseModel):
    status: str = Field(..., pattern="^(success|error)$")
    status_code: int
    message: str
    timestamp: str
    data: Dict[str, Any] = {}
