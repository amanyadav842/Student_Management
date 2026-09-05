from fastapi import FastAPI
from sqlalchemy import text
from .database import engine, Base
from . import models
from .routers import users, students

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind = engine)


app = FastAPI(title = "Student Management API")

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_credentials = True, allow_methods = ["*"], allow_headers=["*"],)

app.include_router(users.router)
app.include_router(students.router)
@app.get("/")
def home():
    return{"message" : "Student Management API is running"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
# @app.get("/")
# def home():
#     return {"message" : "Student Management API is running"}

# @app.get("/test-db")
# def test_db():
#     with engine.connect() as connection:
#         connection.execute(text("SELECT 1"))
#     return {"message" : "Database connected successfully"}