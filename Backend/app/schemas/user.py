from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=20, default="نام")
    lastname: str = Field(min_length=2, max_length=25, default="نام خانوادگی")
    username: str = Field(min_length=3, max_length=35, default="نام کاربری")
    password: str = Field(min_length=8, max_length=100)

class UserUpdate(UserBase):
    phone_number: str = Field(min_length=10, max_length=10)
    email: str
    avatar_url: str = Field(max_length="300")


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=35, default="نام کاربری")
    password: str = Field(min_length=8, max_length=100)


class UserLoginResp(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str



class UserCreate(UserBase):
    id: int
    created_at: datetime.datetime


class User(UserUpdate):
    id: int
    created_at: datetime.datetime
    modified_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None


class UserDeleteRequest(BaseModel):
    ids: List[int]

class Config:
    orm_mode = True
    from_attributes = True



"""
                                    admin Section
"""



class AdminBase(BaseModel):
    name: str
    lastname: str
    username: str
    email: str
    phone: str
    root_access: bool
    password: str
    avatar_link: str

class AdminCreate(AdminBase):
    id: int
    created_at: datetime.datetime

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminLoginResp(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class AdminUpdateResp(AdminBase):
    id:int
    modified_at: datetime.datetime
    google_analyze_website: bool
    instagram_token: str
    google_analytics_token: str