from sqlmodel import Session

def get_session():
    from internal.database.engine import engine
    with Session(engine) as session:
        yield session