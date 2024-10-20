from pydantic import BaseModel, Field
from typing import Optional
import datetime

class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=20, default="نام")
    lastname: str = Field(min_length=2, max_length=25, default="نام خانوادگی")
    username: str = Field(min_length=3, max_length=35, default="نام کاربری")
    password: str = Field(min_length=8, max_length=100)

class UserUpdate(UserBase):
    phone_number: str = Field(min_length="11", max_length="11")
    email: str
    avatar_url: str = Field(max_length="300")


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=35, default="نام کاربری")
    password: str = Field(min_length=8, max_length=100)


class UserLoginResp(BaseModel):
    access_token: str




class UserCreate(UserBase):
    id: int
    created_at: datetime.datetime


class User(UserUpdate):
    id: int
    modified_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None


class Config:
    orm_mode = True
    from_attributes = True