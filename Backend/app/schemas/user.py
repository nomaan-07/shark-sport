from pydantic import BaseModel, Field, AwareDatetime, UUID4
import uuid
from datetime import datetime

class BaseUser(BaseModel):
    name: str
    last_name: str
    username: str
    password: str


class SecondUSer(BaseUser):
    phone: str | None
    email: str | None
    telephone: str | None


class User(BaseUser):
    id : str = Field(default= uuid.uuid4())
    created_at: datetime | None
    modified_at: datetime | None
    deleted_at: datetime | None


class UserLogin(BaseModel):
    username: str
    password: str

class UserAuthenticated(UserLogin):
    id: str = Field(default= uuid.uuid4())

class UserFull(User):
    phone_land: str
    modified_at: datetime

class LoginResponse(BaseModel):
    token: str
    user: UserAuthenticated