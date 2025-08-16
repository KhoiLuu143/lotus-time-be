from models.students import Students
from schemas.students import StudentRead, StudentCreate, StudentUpdate
from fastapi import HTTPException
from sqlmodel import Session, select, func
from datetime import datetime
from models.schedules import Schedules
from models.attendance import Attendance

def get_students(session: Session):
    students = session.exec(select(Students)).all()
    return [StudentRead.model_validate(stu) for stu in students]

def get_student(student_id: str, session: Session):
    student = session.get(Students, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentRead.model_validate(student)

def create_student(student_data: StudentCreate, session: Session):
    new_student = Students(
        user_id=student_data.user_id,
        class_id=student_data.class_id,
    )
    
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    
    return StudentRead.model_validate(new_student)

def update_student(student_id: str, student_data: StudentUpdate, session: Session):
    student = session.get(Students, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)

    session.commit()
    session.refresh(student)
    return StudentRead.model_validate(student)

def delete_student(student_id: str, session: Session):
    student = session.get(Students, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}

def get_student_dashboard_data(session: Session, user_id: str):
    student = session.exec(select(Students).where(Students.user_id == user_id)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_id = student.id
    
    return {
        "role": "STUDENT",
        "class": student.class_id,
        "schedule_count": session.exec(select(Schedules).where(Schedules.class_id == student.class_id)).count(),
        "attended": session.exec(select(Attendance).where(Attendance.student_id == student_id)).count(),
        "attendance_rate": session.exec(select(Attendance).where(Attendance.student_id == student_id)).count() / session.exec(select(Schedules).where(Schedules.class_id == student.class_id)).count() if session.exec(select(Schedules).where(Schedules.class_id == student.class_id)).count() > 0 else 0
    }

def get_student_count(session: Session) -> int:
    return session.exec(select(func.count(Students.id))).one()