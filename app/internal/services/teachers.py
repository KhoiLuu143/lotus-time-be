from fastapi import Depends, HTTPException
from internal.services import teachers as service
from internal.database.session import get_session
from schemas.teachers import TeacherCreate, TeacherUpdate, TeacherRead
from sqlmodel import Session, select, func, distinct
from models.teachers import Teachers
from models.classes import Classes
from models.schedules import Schedules
from models.students import Students
from models.attendance import Attendance
from datetime import datetime

def get_teachers(session: Session = Depends(get_session)):
    return service.get_teachers(session)

def get_teacher(teacher_id: str, session: Session = Depends(get_session)):
    return service.get_teacher(teacher_id, session)

def create_teacher(teacher_data: TeacherCreate, session: Session):
    new_teacher = Teachers(
        name=teacher_data.name,
        subject=teacher_data.subject,
        created_at=datetime.now().isoformat()
    )
    
    session.add(new_teacher)
    session.commit()
    session.refresh(new_teacher)
    
    return TeacherRead.model_validate(new_teacher)

def update_teacher(teacher_id: str, teacher_data: TeacherUpdate, session: Session):
    teacher = session.get(Teachers, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    update_data = teacher_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(teacher, key, value)

    session.commit()
    session.refresh(teacher)
    return TeacherRead.model_validate(teacher)

def delete_teacher(teacher_id: str, session: Session):
    teacher = session.get(Teachers, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    session.delete(teacher)
    session.commit()
    return {"message": "Teacher deleted successfully"}

def get_teacher_dashboard_data(session: Session, user_id: str):
    teacher = session.get(Teachers).where(Teachers.user_id == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher_id = teacher.id
    class_count = session.exec(select(func.count(distinct(Schedules.class_id))).where(Schedules.teacher_id == teacher_id)).one()
    schedule_count = session.exec(select(func.count(Schedules.id)).where((Schedules.teacher_id == teacher_id) and (Schedules.start_time.day == datetime.now().day)))
    
    return {
        "role": "TEACHER",
        "class_count": class_count,
        "student_count": get_teacher_student_count(session, teacher_id),
        "today_schedules": schedule_count,
        "not_checked": get_teacher_not_checked_schedules(session, teacher_id)
    }


# Additional utility functions

def get_teacher_count(session: Session) -> int:
    return session.exec(select(func.count(Teachers.id))).one()

def get_teacher_classes(session: Session, teacher_id: str):
    return session.exec(
        select(distinct(Classes)).join(Schedules)
        .where(Classes.id == Schedules.class_id)
        .where(Schedules.teacher_id == teacher_id)
    ).all()

def get_teacher_student_count(session: Session, teacher_id: str) -> int:
    classes = get_teacher_classes(session, teacher_id)
    student_count = 0
    for cls in classes:
        student_count += session.exec(
            select(func.count(distinct(Students.id)))
            .where(Students.class_id == cls.id)
        ).one()
    return student_count

def get_teacher_schedules(session: Session, teacher_id: str):
    return session.exec(
        select(Schedules).where(Schedules.teacher_id == teacher_id)
    ).all()

def get_teacher_not_checked_schedules(session: Session, teacher_id: str):
    return session.exec(
        select(func.count(distinct(Attendance.id))).join(Schedules)
        .where(Schedules.teacher_id == teacher_id)
        .where(Attendance.status == 'NOT_CHECKED')
    ).one()