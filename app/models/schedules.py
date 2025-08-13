from uuid import UUID as uuid
from uuid import uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field

class Schedules(SQLModel, table = True):
    __tablename__ = "schedules"

    id: uuid = Field(default_factory=uuid4, primary_key=True)
    class_id: uuid = Field(foreign_key="classes.id", nullable=False)
    teacher_id: uuid = Field(foreign_key="teachers.id", nullable=False)
    type: str = Field(nullable=False, default="schedule")
    start_time: datetime = Field(nullable=False)
    end_time: datetime = Field(nullable=False)
    note: str = Field(default="", nullable=True)
    room: uuid = Field(foreign_key="rooms.id", nullable=False)
    ta_id: uuid = Field(foreign_key="teachers.id", nullable=True)

    def __repr__(self):
        return f"<Schedule(id={self.id}, class_id={self.class_id}, teacher_id={self.teacher_id}, start_time={self.start_time}, end_time={self.end_time})>"