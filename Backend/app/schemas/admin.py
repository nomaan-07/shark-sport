from pydantic import BaseModel, AwareDatetime, Field
from datetime import datetime


class BaseAdmin(BaseModel):
    name: str
    lastname: str
    username: str
    email: str
    avatar_link: str
    phone: str
    password: str
    google_analytics_token: str
    instagram_token: str
    google_analyze_website: str
    google_analytics_token: str
    instagram_token: str
    root_access: bool = Field(default=False)

class createAdmin_resp(BaseAdmin):
    id: str
    created_at: datetime

class Admin(BaseAdmin):
    id: str
    created_at: datetime
    modified_at: datetime | None
    deleted_at: datetime | None
    last_login: datetime | None
    root_access: bool


class Login(BaseModel):
    username: str
    password: str


class LoginResp(BaseModel):
    access_token: str



class BasePermission(BaseModel):
    id: int
    admin_id: int
    status: bool = Field()
    description: str

class create_permission_resp(BasePermission):
    creattor_id: int



