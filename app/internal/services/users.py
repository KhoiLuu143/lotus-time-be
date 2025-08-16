from sqlmodel import Session, select, func
from models.users import User
from typing import List, Optional
import uuid
from schemas import users as dto
from fastapi import HTTPException
from internal.services import classes as class_service, teachers as teacher_service, students as student_service, schedules as schedule_service

def get_users(session: Session) -> List[dto.UserRead]:
    users = session.exec(select(User)).all()
    return [dto.UserRead.model_validate(user) for user in users]

def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[dto.UserRead]:
    user = session.get(User, user_id)
    return dto.UserRead.model_validate(user)

def update_user(session: Session, user_id: uuid, new_data: dto.UserUpdate) -> Optional[dto.UserRead]:
    user = session.get(User, user_id)
    if not user:
        return None
    
    update_data = new_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    session.commit()
    session.refresh(user)
    return dto.UserRead.model_validate(user)

def delete_user(session: Session, user_id: uuid.UUID) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

def get_user_dashboard_data(session: Session, user_id: uuid.UUID):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "ADMIN":
        return {
            "role": "ADMIN",
            "user_count": session.exec(select(func.count(User.id))).one() - 1, # Exclude the admin user
            "class_count": class_service.get_class_count(session),
            "teacher_count": teacher_service.get_teacher_count(session),
            "student_count": student_service.get_student_count(session),
            "pending_requests": session.exec(select(func.count(User.id)).where(not User.verified)).one(),
            "today_schedules": schedule_service.get_today_schedules(session)
        }
    elif user.role == "TEACHER":
        return teacher_service.get_teacher_dashboard_data(session, user.id)
    
    elif user.role == "STUDENT":
        return student_service.get_student_dashboard_data(session, user.id)
        
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")