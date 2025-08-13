from fastapi import APIRouter, Depends, HTTPException
from internal.services import students as service
from internal.database.session import get_session
from schemas.students import StudentCreate, StudentUpdate
from sqlmodel import Session
from models.users import User
from dependencies import get_current_user, check_admin

router = APIRouter(prefix="/students")

@router.get("/", summary="Get all students")
def get_students(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.get_students(session)

@router.get("/{student_id}", summary="Get student by ID")
def get_student(student_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.get_student(student_id, session)

@router.post("/", summary="Create a new student")
def create_student(student_data: StudentCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.create_student(student_data, session)

@router.put("/{student_id}", summary="Update a student")
def update_student(student_id: str, student_data: StudentUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.update_student(student_id, student_data, session)

@router.delete("/{student_id}", summary="Delete a student")
def delete_student(student_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return service.delete_student(student_id, session)