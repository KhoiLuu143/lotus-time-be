from models.rooms import Rooms
from fastapi import Depends, HTTPException
from sqlmodel import Session

def get_rooms(session: Session):
    rooms = session.query(Rooms).all()
    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found")
    return rooms

def get_room(room_id: str, session: Session):
    room = session.get(Rooms, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

def create_room(room_data: Rooms, session: Session):
    new_room = Rooms(
        name=room_data.name,
        capacity=room_data.capacity,
        description=room_data.description
    )
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    return new_room

def update_room(room_id: str, room_data: Rooms, session: Session):
    room = session.get(Rooms, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    update_data = room_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)

    session.commit()
    session.refresh(room)
    return room

def delete_room(room_id: str, session: Session):
    room = session.get(Rooms, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    session.delete(room)
    session.commit()
    return {"message": "Room deleted successfully"}
