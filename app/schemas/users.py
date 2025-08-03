from pydantic import BaseModel, EmailStr, constr
from typing import Annotated
from uuid import UUID as uuid
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=6)]
    password_confirm: Annotated[str, constr(min_length=6)]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=6)]

class UserRead(BaseModel):
    id: uuid
    email: EmailStr
    username: str
    full_name: str
    role: str
    is_active: bool = True
    verified: bool = False
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    hashed_password: str
    role: str

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    username: str | None = None
    full_name: str | None = None

    model_config = {
        "from_attributes": True
    }

class UserChangePassword(BaseModel):
    old_password: Annotated[str, constr(min_length=6)]
    new_password: Annotated[str, constr(min_length=6)]
    new_password_confirm: Annotated[str, constr(min_length=6)]

    model_config = {
        "from_attributes": True
    }