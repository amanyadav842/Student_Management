from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentResponse
from app.auth import get_current_user_id

router = APIRouter()

@router.post("/students", response_model = StudentResponse)
def create_student(student: StudentResponse, user_id : int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    new_student = Student(name  = student.name, branch = student.branch, owner_id = user_id)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/students/{student_id}", response_model = StudentResponse)
def get_students(student_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id, Student.owner_id == user_id).first()

    if student is None:
        raise HTTPException(status_code = 404, detail = "Student not found")
    return student

@router.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(
        Student.id == student_id,
        Student.owner_id == user_id
    ).first()

    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db_student.name = student.name
    db_student.branch = student.branch

    db.commit()
    db.refresh(db_student)

    return db_student

@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(
        Student.id == student_id,
        Student.owner_id == user_id
    ).first()

    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(db_student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }