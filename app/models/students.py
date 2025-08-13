from uuid import UUID as uuid
from uuid import uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field

class Students(SQLModel, table=True):
    __tablename__ = "students"
    
    id: uuid = Field(default_factory=uuid4, primary_key=True)
    class_id: uuid = Field(foreign_key="classes.id", nullable=False)
    user_id: uuid = Field(foreign_key="users.id", nullable=False)

    