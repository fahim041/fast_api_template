from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: int
    email: str
    created_at: datetime

    class config:
        orm_mode = True

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner: User

    class config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    token: str
    token_type: str


class UserTokenData(BaseModel):
    id: int
    email: EmailStr