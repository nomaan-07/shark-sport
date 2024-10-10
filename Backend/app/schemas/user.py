from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    lastname: str
    username: str
    password: str

class CreateResp(UserBase):
    avatar_link: str
    id: int
    created_at: datetime


class Login(BaseModel):
    username: str
    password: str


class LoginResp(BaseModel):
    access_token: str
    refresh_token: str
    user: dict
    

class User(CreateResp):
    avatar_link: str
    email: str
    phone_number: str
    modified_at: datetime
    deleted_at: datetime

