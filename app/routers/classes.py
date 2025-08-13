from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from schemas.classes import ClassCreate, ClassRead, ClassUpdate
from internal.services import classes as service
from internal.database.session import get_session
from models.users import User
from dependencies import get_current_user, check_admin

router = APIRouter(prefix="/classes")

@router.get("/", summary="Get all classes")
def get_classes(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.get_classes(session)

@router.get("/{class_id}", summary="Get class by ID")
def get_class(class_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.get_class(class_id, session)

@router.post("/", summary="Create a new class")
def create_class(class_data: ClassCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.create_class(class_data, session)

@router.put("/{class_id}", summary="Update a class")
def update_class(class_id: str, class_data: ClassUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.update_class(class_id, class_data, session)

@router.delete("/{class_id}", summary="Delete a class")
def delete_class(class_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.delete_class(class_id, session)