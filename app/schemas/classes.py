from pydantic import BaseModel
from uuid import UUID as uuid
from datetime import datetime

class ClassCreate(BaseModel):
    name: str
    type: str
    num_hours: int
    description: str | None = None

class ClassRead(BaseModel):
    id: uuid
    name: str
    type: str
    num_hours: int
    description: str | None = None
    created_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }

class ClassUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    num_hours: int | None = None
    description: str | None = None