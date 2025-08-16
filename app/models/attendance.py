from sqlmodel import SQLModel, Field
from uuid import UUID as uuid
from uuid import uuid4
from datetime import datetime

class Attendance(SQLModel, table=True):
    id: uuid = Field(default_factory=uuid4, primary_key=True)
    student_id: str = Field(foreign_key="students.id")
    schedule_id: str = Field(foreign_key="schedules.id")
    status: str  # e.g., "present", "absent", "late"
    marked_by: str = Field(foreign_key="users.id")
    marked_at: datetime = Field(default_factory=datetime.now)