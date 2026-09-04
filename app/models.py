from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True,)
    email = Column(String, unique = True, index= True, nullable=False)
    password_hash = Column(String, nullable=False)

    students = relationship("Student", back_populates="owner")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, nullable=False)
    branch = Column(String, nullable= False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="students")