from fastapi import Depends, HTTPException
from internal.services import teachers as service
from internal.database.session import get_session
from schemas.teachers import TeacherCreate, TeacherUpdate, TeacherRead
from sqlmodel import Session
from models.teachers import Teachers
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