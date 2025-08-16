from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.attendance import Attendance
from schemas.attendance import AttendanceCreate, AttendanceUpdate
from internal.services import attendance as service
from internal.database.session import get_session
from dependencies import get_current_user
from models.users import User

router = APIRouter(prefix="/attendance")

@router.get("/", summary="Get all attendance records", response_model=list[Attendance])
def read_attendance(session: Session = Depends(get_session)):
    return service.get_attendances(session)

@router.get("/{attendance_id}", summary="Get attendance record by id", response_model=Attendance)
def read_attendance_by_id(attendance_id: str, session: Session = Depends(get_session)):
    attendance = service.get_attendance(attendance_id, session)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance

@router.post("/", summary="Create a new attendance record", response_model=Attendance)
def create_attendance(attendance_data: AttendanceCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return service.create_attendance(attendance_data, session, user_id=current_user.id)

@router.put("/{attendance_id}", summary="Update an attendance record", response_model=Attendance)
def update_attendance(attendance_id: str, attendance_data: AttendanceUpdate, session: Session = Depends(get_session)):
    attendance = service.update_attendance(attendance_id, attendance_data, session)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance

@router.delete("/{attendance_id}", summary="Delete an attendance record")
def delete_attendance(attendance_id: str, session: Session = Depends(get_session)): 
    success = service.delete_attendance(attendance_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return {"message": "Attendance record deleted successfully"}

