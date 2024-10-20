from pydantic import BaseModel, AwareDatetime, Field
from datetime import datetime
from fastapi import UploadFile

class BaseAdmin(BaseModel):
    name: str
    lastname: str
    username: str
    email: str
    avatar_link: str
    phone: str
    password: str
    google_analytics_token: str | None
    instagram_token: str | None
    google_analyze_website: bool
    google_analytics_token: str | None
    instagram_token: str | None
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



class SchemaAdminUpdate(BaseModel):
    name: str | None 
    lastname: str | None
    username: str | None
    email: str | None
    phone: str | None
    google_analytics_token: str | None
    google_analyze_website: bool | None
    instagram_token: str | None
    root_access: bool | None
    password: str | None
    avatar: UploadFile | None