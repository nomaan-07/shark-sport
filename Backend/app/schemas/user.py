from pydantic import BaseModel, Field, AwareDatetime, UUID4
import uuid
from datetime import datetime

class UserBase(BaseModel):
    name: str
    last_name: str
    username: str
    password: str

class User(UserBase):
    id : str = Field(default= uuid.uuid4())
    created_at: datetime = Field(default=datetime.now().replace(second=0, microsecond=0))

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