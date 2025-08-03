from sqlmodel import Session, select
from models.users import User
from typing import List, Optional
import uuid
from schemas import users as dto

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