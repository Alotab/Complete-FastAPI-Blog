from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime




class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int 
    email: EmailStr
    # created_at: datetime


    class Config:
    #    orm_mode = True
       from_attributes = True