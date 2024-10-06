# models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    code: str
    weight: str
    fabric_type: str
    pattern: str
    color: str
    size_options: List[str]
    price: int
    seller_id: Optional[int]
    image_urls: List[str]

class ProductResponse(ProductCreate):
    id: int
    created_at: datetime | None
    updated_at: datetime | None