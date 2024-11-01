from pydantic import BaseModel, Field
import datetime
from typing import Annotated, Optional


class NotificationBase(BaseModel):
    message: str = Field(max_length=300)
    subject: str = Field(max_length=100)

class UserNotification(NotificationBase):
    user_id: int
    read_status: bool

class AdminNotification(NotificationBase):
    admin_id: int
    read_status: bool




class Notification(BaseModel):
    id: Optional[int] = None
    message: str
    subject: str
    user_id: Optional[int] = None
    admin_id: Optional[int] = None
    read_status: bool = False
    created_at: datetime.datetime
