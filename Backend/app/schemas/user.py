from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    lastname: str
    username: str
    password: str


class UserCreateResp(UserBase):
    id: int
    created_at: datetime


class UserUpdate(UserBase):
    id: int
    avatar_link: str
    modified_at: datetime

class Login(BaseModel):
    username: str
    password: str


class LoginResp(BaseModel):
    access_token: str
    refresh_token: str
    uid: int
    

class User(UserUpdate):
    email: str
    phone_number: str
    deleted_at: Optional[datetime] = None
    created_at: datetime

