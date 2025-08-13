from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.rooms import Rooms
from internal.services import rooms as service
from internal.database.session import get_session

router = APIRouter(prefix="/rooms")

@router.get("/", summary="Get all rooms")
def get_rooms(session: Session = Depends(get_session)):
    return service.get_rooms(session)

@router.get("/{room_id}", summary="Get room by ID")
def get_room(room_id: str, session: Session = Depends(get_session)):
    return service.get_room(room_id, session)

@router.post("/", summary="Create a new room")
def create_room(room_data: Rooms, session: Session = Depends(get_session)):
    return service.create_room(room_data, session)

@router.put("/{room_id}", summary="Update a room")
def update_room(room_id: str, room_data: Rooms, session: Session = Depends(get_session)):
    return service.update_room(room_id, room_data, session)

@router.delete("/{room_id}", summary="Delete a room")
def delete_room(room_id: str, session: Session = Depends(get_session)):
    return service.delete_room(room_id, session)