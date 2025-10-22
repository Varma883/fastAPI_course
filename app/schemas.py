from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int

    model_config = ConfigDict(from_attributes=True)  # ✅ Pydantic v2 ORM support


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id :int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    user_id : int
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] =None
