from fastapi import APIRouter, Depends, HTTPException
from internal.services import teachers as service
from sqlmodel import Session
from internal.database.session import get_session
from schemas.teachers import TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/teachers")

@router.get("/", summary="Get all teachers")
def get_teachers(session: Session = Depends(get_session)):
    return service.get_teachers(session)

@router.get("/{teacher_id}", summary="Get teacher by ID")
def get_teacher(teacher_id: str, session: Session = Depends(get_session)):
    return service.get_teacher(teacher_id, session)

@router.post("/", summary="Create a new teacher")
def create_teacher(teacher_data: TeacherCreate, session: Session = Depends(get_session)):
    return service.create_teacher(teacher_data, session)

@router.put("/{teacher_id}", summary="Update a teacher")
def update_teacher(teacher_id: str, teacher_data: TeacherUpdate, session: Session = Depends(get_session)):
    return service.update_teacher(teacher_id, teacher_data, session)

@router.delete("/{teacher_id}", summary="Delete a teacher")
def delete_teacher(teacher_id: str, session: Session = Depends(get_session)):
    return service.delete_teacher(teacher_id, session)