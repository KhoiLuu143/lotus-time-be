from uuid import UUID as uuid
from pydantic import BaseModel
from datetime import datetime

class ScheduleRead(BaseModel):
    id: str
    class_id: str
    teacher_id: str
    room_id: str
    start_time: datetime
    end_time: datetime
    note: str | None = None
    ta_id: str | None = None
    type: str = "schedule"
   
    model_config = {
        "from_attributes": True
    }

class ScheduleCreate(BaseModel):
    class_id: uuid
    teacher_id: uuid
    room_id: uuid
    start_time: datetime
    end_time: datetime
    note: str | None = None
    ta_id: uuid | None = None

class ScheduleUpdate(BaseModel):
    class_id: uuid | None = None
    teacher_id: uuid | None = None
    room_id: uuid | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    note: str | None = None
    ta_id: uuid | None = None

    model_config = {
        "from_attributes": True
    }