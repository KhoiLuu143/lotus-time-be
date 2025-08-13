from sqlmodel import SQLModel, Field
from uuid import UUID as uuid
from uuid import uuid4

class Rooms(SQLModel, table=True):
    __tablename__ = "rooms"

    id: uuid = Field(primary_key=True, index=True, default_factory=uuid4)
    name: str = Field(index=True)

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name})>"