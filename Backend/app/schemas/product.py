from pydantic import BaseModel
from datetime import datetime
from typing import Union


class BaseProduct(BaseModel):
    product_code: str
    name: str
    description: str
    category_id: str


class Product(BaseProduct):
    id: str
    created_at: datetime
    modified_at: datetime | None
    deleted_at: datetime | None


class BaseProductCategory(BaseModel):
   id: str
   name: str
   description: str


class ProductCategory(BaseProductCategory):
    created_at: datetime
    modified_at: datetime | None
    deleted_at: datetime | None


class BaseAttributes(BaseModel):
    product_id: str
    price : str
    offer_price : str
    tags : str
    brand : str
    attributes : str
    dimensions : str
    weight : str


class Atrributes(BaseAttributes):
    id: str
    created_at: datetime
    modified_at: datetime
    deleted_at: datetime


class Image(BaseModel):
    id: str
    url: str
    created_at: datetime | None
    deleted_at: datetime | None