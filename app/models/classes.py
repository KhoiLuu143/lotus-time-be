from sqlmodel import SQLModel, Field
from uuid import UUID as uuid
from uuid import uuid4
from datetime import datetime

class Classes(SQLModel, table=True):
    __tablename__ = "classes"
    
    id: uuid = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    type: str = Field(nullable=False, default="class")
    num_hours: int = Field(default=0, nullable=False)
    description: str = Field(default="", nullable=True)
    created_at: datetime = Field(default=None, nullable=True)

    def __repr__(self):
        return f"Classes(id={self.id}, name={self.name}, type={self.type}, num_hours={self.num_hours})"