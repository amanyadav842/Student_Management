from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class config:
        from_attributes = True

class StudentCreate(BaseModel):
    name : str = Field(min_length=2, max_length=100)
    branch: str = Field(min_length=2, max_length=50)

class StudentResponse(BaseModel):
    id: int
    name: str
    branch: str

    class config:
        from_attributes = True