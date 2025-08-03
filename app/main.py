from fastapi import FastAPI

from routers import users
from routers import auth

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(auth.router, prefix="/api", tags=["auth"])