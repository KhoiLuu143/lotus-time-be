from uuid import UUID as uuid
from pydantic import BaseModel

class TeacherRead(BaseModel):
    id: str
    name: str
    email: str
    subject: str

class TeacherCreate(BaseModel):
    name: str
    email: str
    subject: str

class TeacherUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    subject: str | None = None

    model_config = {
        "from_attributes": True
    }