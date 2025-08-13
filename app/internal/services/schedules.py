from datetime import datetime
from uuid import UUID as uuid
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from internal.database.session import get_session
from schemas.schedules import ScheduleCreate, ScheduleUpdate
from models.schedules import Schedules

def get_schedules(session: Session):
    schedules = session.query(Schedules).all()
    return schedules

def get_schedule(schedule_id: str, session: Session):
    schedule = session.query(Schedules).filter(Schedules.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

def create_schedule(schedule_data: ScheduleCreate, session: Session):
    new_schedule = Schedules(
        class_id=schedule_data.class_id,
        teacher_id=schedule_data.teacher_id,
        room_id=schedule_data.room_id,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time,
        created_at=datetime.now().isoformat()
    )
    
    session.add(new_schedule)
    session.commit()
    session.refresh(new_schedule)
    
    return new_schedule

def update_schedule(schedule_id: str, schedule_data: ScheduleUpdate, session: Session):
    schedule = session.query(Schedules).filter(Schedules.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    update_data = schedule_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(schedule, key, value)

    session.commit()
    session.refresh(schedule)
    return schedule

def delete_schedule(schedule_id: str, session: Session):
    schedule = session.query(Schedules).filter(Schedules.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    session.delete(schedule)
    session.commit()
    return {"message": "Schedule deleted successfully"}
