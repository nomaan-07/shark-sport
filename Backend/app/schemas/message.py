from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class UserLogoutMessage(BaseModel):
    message: str


class UserAuthDict(BaseModel):
    uid: int
    user_type: str
    refresh: bool

class UserGetMe(BaseModel):
    name: str 
    lastname: str 
    username: str 
    email: Optional[str] = None 
    phone: Optional[str] = None 
    avatar_url: Optional[str] = None

class UserGetMessage(BaseModel):
    auth_dict : UserAuthDict
    user: UserGetMe


class AdminAuthDict(UserAuthDict):
    root_access: bool
class AdminGet(UserGetMe):
    google_analytics_token: Optional[str] = None
    instagram_token: Optional[str] = None
    google_analyze_website: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    modified_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class AdminGetMe(BaseModel):
    auth_dict: AdminAuthDict
    admin: AdminGet