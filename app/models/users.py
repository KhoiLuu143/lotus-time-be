from uuid import UUID as uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    full_name: str = Field(nullable=False, default="")
    is_active: bool = Field(default=True, nullable=False)
    verified: bool = Field(default=False, nullable=False)
    password_hash: str = Field(default=None, nullable=False)
    role: str = Field(nullable=False, default="USER")
    created_at: datetime = Field(default=None, nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"