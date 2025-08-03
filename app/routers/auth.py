from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session
from schemas import users as dto
from internal.services import auth as service
from internal.database.session import get_session
from dependencies import get_current_user
from models.users import User
import util

router = APIRouter(prefix="/auth")

@router.post("/register", summary="Register")
async def register(user: dto.UserRegister):
    return await service.register(user)

@router.get("/verify-email/{token}", summary="Verify email")
def verify_email(token: str, session: Session = Depends(get_session)):
    return service.verify_email(token, session)

@router.post("/complete-registration", summary="Complete registration")
def complete_registration(user: dto.UserCreate, session: Session = Depends(get_session)):
    return service.complete_registration(user, session)

@router.post("/login", summary="Login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    db_user = service.login(username, password, session)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = util.create_access_token(data={"sub": db_user.username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/forgot-password", summary="Forgot password")
async def forgot_password(email: str, session: Session = Depends(get_session)):
    return await service.forgot_password(email, session)

@router.post("/reset-password", summary="Reset password")
def reset_password(
    token: str = Form(...),
    new_password: str = Form(...),
    session: Session = Depends(get_session)
):
    return service.reset_password(token, new_password, session)

@router.post("/change-password", summary="Change password")
def change_password(
    user_change: dto.UserChangePassword,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        if not util.verify_password(user_change.old_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Old password is incorrect")

        if user_change.new_password != user_change.new_password_confirm:
            raise HTTPException(status_code=400, detail="New passwords do not match")
        
        user = service.change_password(current_user, user_change.new_password, session)
        if not user:
            raise HTTPException(status_code=400, detail="Update password failed")
        
        return {"message": "Password changed successfully", "user": dto.UserRead.model_validate(user)}
    except HTTPException as e:
        raise e