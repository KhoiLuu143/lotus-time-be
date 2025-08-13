from datetime import datetime
from uuid import UUID as uuid
from pydantic import BaseModel

class ActionLogRead(BaseModel):
    id: uuid
    action: str
    user_id: int
    target_type: str
    target_id: uuid
    details: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

class ActionLogCreate(BaseModel):
    action: str
    user_id: int
    target_type: str = None
    target_id: uuid = None
    details: str = None
