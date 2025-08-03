from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

DATABASE_URL = "postgresql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + ":5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)