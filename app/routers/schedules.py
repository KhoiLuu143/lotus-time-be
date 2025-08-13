from fastapi import Depends, HTTPException
from sqlmodel import Session
from internal.services import schedules as service
from internal.database.session import get_session
from schemas.schedules import ScheduleCreate, ScheduleUpdate
from fastapi import APIRouter

router = APIRouter(prefix="/schedules")

@router.get("/", summary="Get all schedules")
def get_schedules(session: Session = Depends(get_session)):
    return service.get_schedules(session)

@router.get("/{schedule_id}", summary="Get schedule by ID")
def get_schedule(schedule_id: str, session: Session = Depends(get_session)):
    return service.get_schedule(schedule_id, session)

@router.post("/", summary="Create a new schedule")
def create_schedule(schedule_data: ScheduleCreate, session: Session = Depends(get_session)):
    return service.create_schedule(schedule_data, session)

@router.put("/{schedule_id}", summary="Update a schedule")
def update_schedule(schedule_id: str, schedule_data: ScheduleUpdate, session: Session = Depends(get_session)):
    return service.update_schedule(schedule_id, schedule_data, session)

@router.delete("/{schedule_id}", summary="Delete a schedule")
def delete_schedule(schedule_id: str, session: Session = Depends(get_session)):
    return service.delete_schedule(schedule_id, session)
