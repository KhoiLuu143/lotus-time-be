from fastapi import APIRouter
from internal.services import action_logs as service
from fastapi import Depends, HTTPException
from sqlmodel import Session
from internal.database.session import get_session
from schemas.action_logs import ActionLogCreate

router = APIRouter(prefix="/action_logs")

@router.get("/", summary="Get all action logs")
def get_action_logs(session: Session = Depends(get_session)):
    return service.get_action_logs(session)

@router.get("/{log_id}", summary="Get action log by ID")
def get_action_log(log_id: str, session: Session = Depends(get_session)):
    log = service.get_action_log(log_id, session)
    if not log:
        raise HTTPException(status_code=404, detail="Action log not found")
    return log

@router.post("/", summary="Create a new action log")
def create_action_log(log_data: ActionLogCreate, session: Session = Depends(get_session)):
    return service.create_action_log(log_data, session)

@router.put("/{log_id}", summary="Update an action log")
def update_action_log(log_id: str, log_data: ActionLogCreate, session:  Session = Depends(get_session)):
    log = service.update_action_log(log_id, log_data, session)
    if not log:
        raise HTTPException(status_code=404, detail="Action log not found")
    return log

@router.delete("/{log_id}", summary="Delete an action log")
def delete_action_log(log_id: str, session: Session = Depends(get_session)):
    success = service.delete_action_log(log_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Action log not found")
    return {"detail": "Action log deleted successfully"}