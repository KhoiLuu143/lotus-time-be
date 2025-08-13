from datetime import datetime
from sqlmodel import Session, select
from schemas.action_logs import ActionLogRead, ActionLogCreate
from models.action_logs import ActionLogs

def get_action_logs(session: Session):
    logs = session.exec(select(ActionLogs)).all()
    return [ActionLogRead.model_validate(log) for log in logs]

def get_action_log(log_id: str, session: Session):
    log = session.get(ActionLogs, log_id)
    if not log:
        return None
    return ActionLogRead.model_validate(log)

def create_action_log(log_data: ActionLogCreate, session: Session):
    new_log = ActionLogs(
        action=log_data.action,
        user_id=log_data.user_id,
        target_type=log_data.target_type,
        target_id=log_data.target_id,
        details=log_data.details,
        timestamp=datetime.now()
    )
    session.add(new_log)
    session.commit()
    session.refresh(new_log)
    return ActionLogRead.model_validate(new_log)

def update_action_log(log_id: str, log_data: ActionLogCreate, session: Session):
    log = session.get(ActionLogs, log_id)
    if not log:
        return None
    
    update_data = log_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(log, key, value)

    session.commit()
    session.refresh(log)
    return ActionLogRead.model_validate(log)

def delete_action_log(log_id: str, session: Session):
    log = session.get(ActionLogs, log_id)
    if not log:
        return False
    
    session.delete(log)
    session.commit()
    return True