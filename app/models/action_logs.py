from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID as uuid

class ActionLogs(SQLModel, table=True):
    __tablename__ = "action_logs"

    id: uuid = Field(primary_key=True, index=True, default_factory=uuid4)
    action: str = Field(index=True)
    user_id: int = Field(index=True)
    target_type: str = Field(index=True, nullable=True)
    target_id: uuid = Field(index=True, nullable=True)
    details: str = Field(default=None, nullable=True)
    timestamp: datetime = Field(default_factory=datetime.now, index=True)

    def __repr__(self):
        return f"<ActionLogs(id={self.id}, action={self.action}, user_id={self.user_id}, target_type={self.target_type}, target_id={self.target_id}, timestamp={self.timestamp})>"