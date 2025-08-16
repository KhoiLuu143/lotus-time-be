from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    id: str
    student_id: str
    schedule_id: str
    status: str  # e.g., "present", "absent", "late"
    timestamp: datetime

class AttendanceRead(BaseModel):
    id: str
    student_id: str
    schedule_id: str
    status: str  # e.g., "present", "absent", "late"
    marked_by: str
    marked_at: datetime

    model_config = {
        "from_attributes": True
    }

class AttendanceUpdate(BaseModel):
    status: str | None = None  # e.g., "present", "absent", "late"