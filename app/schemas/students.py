from uuid import UUID as uuid
from pydantic import BaseModel

class StudentRead(BaseModel):

    id: uuid
    class_id: uuid
    user_id: uuid

    model_config = {
        "from_attributes": True
    }

class StudentCreate(BaseModel):
    class_id: uuid
    user_id: uuid

class StudentUpdate(BaseModel):
    class_id: uuid | None = None