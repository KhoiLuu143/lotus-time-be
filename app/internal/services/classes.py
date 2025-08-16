from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from schemas.classes import ClassCreate, ClassRead, ClassUpdate
from models.classes import Classes
from uuid import UUID as uuid 
from datetime import datetime

def get_classes(session: Session):
    classes = session.exec(select(Classes)).all()
    return [ClassRead.model_validate(cls) for cls in classes]

def get_class(class_id: str, session: Session):
    cls = session.get(Classes, class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    return ClassRead.model_validate(cls)

def create_class(class_data: ClassCreate, session: Session):
    new_class = Classes(
        name=class_data.name,
        type=class_data.type,
        num_hours=class_data.num_hours,
        description=class_data.description,
        created_at=datetime.now().isoformat()
    )
    session.add(new_class)
    session.commit()
    session.refresh(new_class)
    return ClassRead.model_validate(new_class)

def update_class(class_id: str, class_data: ClassUpdate, session: Session):
    cls = session.get(Classes, class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    
    update_data = class_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cls, key, value)

    session.commit()
    session.refresh(cls)
    return ClassRead.model_validate(cls)

def delete_class(class_id: str, session: Session):
    cls = session.get(Classes, class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    
    session.delete(cls)
    session.commit()
    return {"message": "Class deleted successfully"}

def get_class_count(session: Session) -> int:
    return session.exec(select(func.count(Classes.id))).one()