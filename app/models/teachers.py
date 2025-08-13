from sqlmodel import SQLModel, Field
from uuid import UUID as uuid
from uuid import uuid4

class Teachers(SQLModel, table=True):
    __tablename__ = "teachers"

    id: uuid = Field(default_factory=uuid4, primary_key=True)
    type: str = Field(nullable=False)
    salary_rate: float = Field(nullable=False)
    teach_time: int = Field(nullable=False)
    user_id: uuid = Field(foreign_key="users.id", nullable=False)

    def __repr__(self):
        return f"Teacher(id={self.id}, type={self.type}, salary_rate={self.salary_rate}, teach_time={self.teach_time}, user_id={self.user_id})"