from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session
from models.users import User
from schemas import users as dto
from internal.services import users as service
from internal.database.session import get_session
from dependencies import get_current_user

router = APIRouter(prefix="/users")

@router.get("/", summary="Get all users", response_model=list[dto.UserRead])
def read_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return service.get_users(session)

@router.get("/{user_id}", summary="Get user by id", response_model=dto.UserRead)
def read_user(user_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = service.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me", summary="Get current user", response_model=dto.UserRead)
def read_current_user(user: User = Depends(get_current_user)):
    return user

@router.put("/me", summary="Update current user", response_model=dto.UserRead)
def update_current_user(user_data: dto.UserUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    user_db = service.update_user(session, current_user.id, user_data)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db

@router.delete("/{user_id}", summary="Delete user")
def delete_user(user_id: str, session: Session = Depends(get_session)):
    success = service.delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Deleted"}

