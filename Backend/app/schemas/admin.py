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
    id: int
    created_at: datetime

class Admin(BaseAdmin):
    id: int
    created_at: datetime
    modified_at: datetime
    deleted_at: datetime
    last_login: datetime
    root_access: datetime


class Login(BaseModel):
    username: str
    password: str


class LoginResp(BaseModel):
    pass



class BasePermission(BaseModel):
    id: int
    admin_id: int
    status: bool = Field()
    description: str

class create_permission_resp(BasePermission):
    creattor_id: int