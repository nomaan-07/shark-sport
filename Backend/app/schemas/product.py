from pydantic import BaseModel
import datetime
from typing import Optional



class ProductBase(BaseModel):
    images_urls: list[str]
    name: str
    description: str
    survay: str
    original_price: int
    discount_id: int
    category_id: int
    brand: int
    warranty: str


class ProductCreate(ProductBase):
    id: int
    created_at: datetime.datetime
    price_after_discount: int
    attributes: list[str]
    tags: list[str]

class Product(ProductCreate):
    modified_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""----------------------------------------discount Section----------------------------"""



class CategoryBase(BaseModel):
    name: str
    image_url: str
    description: Optional[str]


class CategoryCreate(CategoryBase):
    id: int
    created_at: datetime.datetime


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


class Category(CategoryCreate):
    modified_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None




"""----------------------------------------discount Section----------------------------"""



class DiscountBase(BaseModel):
    name: str
    discount_code: str
    discount_rate: int
    expires_at: datetime.datetime

class Discount(DiscountBase):
    id: int
    created_at: datetime.datetime

