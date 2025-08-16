from sqlmodel import Session, select
from fastapi import HTTPException
from schemas.attendance import AttendanceCreate, AttendanceRead, AttendanceUpdate
from models.attendance import Attendance
from uuid import UUID as uuid
from datetime import datetime

def get_attendances(session: Session):
    attendance_records = session.exec(select(Attendance)).all()
    return [Attendance.model_validate(record) for record in attendance_records]

def get_attendance(attendance_id: str, session: Session):
    attendance = session.get(Attendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return Attendance.model_validate(attendance)

def create_attendance(attendance_data: AttendanceCreate, session: Session, user_id: uuid):
    new_attendance = Attendance(
        student_id=attendance_data.student_id,
        schedule_id=attendance_data.schedule_id,
        status=attendance_data.status,
        marked_by=user_id,
        marked_at=datetime.now().isoformat()
    )
    session.add(new_attendance)
    session.commit()
    session.refresh(new_attendance)
    return Attendance.model_validate(new_attendance)

def update_attendance(attendance_id: str, attendance_data: AttendanceUpdate, session: Session):
    attendance = session.get(Attendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    update_data = attendance_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(attendance, key, value)

    session.commit()
    session.refresh(attendance)
    return Attendance.model_validate(attendance)

def delete_attendance(attendance_id: str, session: Session):
    attendance = session.get(Attendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    session.delete(attendance)
    session.commit()
    return {"message": "Attendance record deleted successfully"}