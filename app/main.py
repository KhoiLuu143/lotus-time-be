from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, auth, classes, students, teachers, rooms, schedules, action_logs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các methods
    allow_headers=["*"],  # Cho phép tất cả các headers
)

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(classes.router, prefix="/api", tags=["classes"])
app.include_router(students.router, prefix="/api", tags=["students"])
app.include_router(teachers.router, prefix="/api", tags=["teachers"])
app.include_router(rooms.router, prefix="/api", tags=["rooms"])
app.include_router(schedules.router, prefix="/api", tags=["schedules"])
app.include_router(action_logs.router, prefix="/api", tags=["action_logs"])