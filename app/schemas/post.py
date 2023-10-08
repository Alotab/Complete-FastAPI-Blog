from pydantic import BaseModel
from datetime import datetime
from .user import UserOut


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
    #    orm_mode = True
       from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
    #    orm_mode = True
       from_attributes = True