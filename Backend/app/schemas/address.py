from pydantic import BaseModel, Field, AwareDatetime, UUID4
import uuid
from datetime import datetime




class BaseAddress(BaseModel):
    province: str
    city: str
    postal_code: str
    detail: str


class Address(BaseAddress):
    id: str
    created_at: datetime | None
    modified_at: datetime | None
    deleted_at: datetime | None

    