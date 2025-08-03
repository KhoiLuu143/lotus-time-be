import util
import mail
from uuid import UUID as uuid
from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import datetime
from sqlmodel import Session, select
from models.users import User
from schemas import users as dto

async def register(user_reg: dto.UserRegister):
    if user_reg.password != user_reg.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    # validate email
    pw = util.get_password_hash(user_reg.password)
    data={
        "sub": user_reg.email,
        "hashed_password": pw
    }
    token = util.create_access_token(data)
    try:
        await mail.send_email(user_reg.email, token)
        return {"message": "Email đã được gửi để xác thực"}
    except Exception as e:
        print(f"Email sending failed: {e}")
        raise HTTPException(status_code=500, detail="Không thể gửi email")

def verify_email(token: str, session: Session):
    try:
        payload = jwt.decode(token, util.SECRET_KEY, algorithms=[util.ALGORITHM])
        email = payload.get("sub")
        hashed_password = payload.get("hashed_password")
        
        if not email or not hashed_password:
            raise HTTPException(404, "User not found")
         
        # check if user already exists
        existing_user = session.exec(select(User).where(User.email == email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email đã được sử dụng")
        
        return {
            "message": "Xác thực email thành công!",
            "verified": True,
            "email": email,
            "hashed_password": hashed_password,
            "verified_at": datetime.now().isoformat()
        }
    
    except JWTError:
        raise HTTPException(400, "Token không hợp lệ hoặc đã hết hạn")
    
def complete_registration(user: dto.UserCreate, session: Session) -> dto.UserRead: 
    try:
        new_user = User(
            id=uuid.uuid4(),
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            password_hash=user.hashed_password,
            role=user.role if user.role else "user",
            is_active=True,
            verified=True,
            created_at=datetime.now().isoformat()
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return dto.UserRead.model_validate(new_user)
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

def login(email: str, password: str, session: Session) -> dto.UserRead:
    # get user
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return None
    # verify password
    if util.verify_password(password, user.password_hash):
        return dto.UserRead.model_validate(user)
    return None

async def forgot_password(email: str, session: Session):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate reset token
    token = util.create_access_token(data={"sub": user.email})
    
    try:
        # Send reset email
        await mail.send_reset_email(user.email, token)
        return {"message": "Reset password email sent"}
    except Exception as e:
        print(f"Email sending failed: {e}")
        raise HTTPException(status_code=500, detail="Can not send email")
    
def reset_password(token: str, new_password: str, session: Session):
    try:
        payload = jwt.decode(token, util.SECRET_KEY, algorithms=[util.ALGORITHM])
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(400, "Invalid token")
        
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(404, "User not found")
        
        # Update password
        user.password_hash = util.get_password_hash(new_password)
        session.add(user)
        session.commit()
        
        return {"message": "Password reset successful"}
    
    except JWTError:
        raise HTTPException(400, "Token is invalid or has expired")
    
def change_password(user: User, new_password: str, session: Session):
    user.password_hash = util.get_password_hash(new_password)
    session.commit()
    session.refresh(user)
    return user