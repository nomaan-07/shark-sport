from pydantic import BaseModel

class UserLogoutMessage(BaseModel):
    message: str