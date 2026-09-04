from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm


from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse

from ..auth import create_access_token
from ..auth import get_current_user_id

router = APIRouter(prefix = "/users", tags = ["Users"])

password_hash = PasswordHash.recommended()

def hash_password(password):
    return password_hash.hash(password)

@router.post("/register", response_model = UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code= 400, detail="Email already registerd")
    hashed_password = hash_password(user.password)

    new_user = User(email = user.email, password_hash = hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == from_data.username).first()

    if db_user is None:
        raise HTTPException(status_code = 401, detail="Invalid email or password")

    if not password_hash.verify(from_data.password, db_user.password_hash):
        raise HTTPException(status_code = 401, detail= "Invalid email or password")
    access_token = create_access_token(db_user.id)

    return {"access_token": access_token, "token_type":"bearer"}
    

@router.get("/me", response_model = UserResponse)
def get_me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user   