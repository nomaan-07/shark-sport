from pydantic import BaseModel
import datetime
from typing import Annotated, List



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
    modified_at: Annotated[None,datetime.datetime] = None
    deleted_at: Annotated[None,datetime.datetime] = None




class ProductResponse(BaseModel):
    id: int
    name: str
    description: Annotated[None,str] = None
    survey: Annotated[None,str] = None
    original_price: int
    price_after_discount: float
    warranty: Annotated[None,str] = None
    discount_id: int
    category_id: int 
    brand: Annotated[None,str]
    created_at: str  # Adjust type as necessary (e.g., datetime)

class SpecificationResponse(BaseModel):
    name: str
    description: str

class SizeResponse(BaseModel):
    size: str
    color: str
    quantity: int

class CreateProductResponse(BaseModel):
    product: ProductResponse
    tags: List[str]
    specifications: List[SpecificationResponse]
    sizes: List[SizeResponse]
    images: List[str]

"""----------------------------------------discount Section----------------------------"""



class CategoryBase(BaseModel):
    name: str
    image_url: str
    description: Annotated[None,str]


class CategoryCreate(CategoryBase):
    id: int
    created_at: datetime.datetime


class CategoryUpdate(BaseModel):
    name: Annotated[None,str] = None
    image_url: Annotated[None,str] = None
    description: Annotated[None,str] = None


class Category(CategoryCreate):
    modified_at: Annotated[None,datetime.datetime] = None
    deleted_at: Annotated[None,datetime.datetime] = None




"""----------------------------------------discount Section----------------------------"""



class DiscountBase(BaseModel):
    name: str
    discount_code: str
    discount_rate: int
    expires_at: datetime.datetime

class Discount(DiscountBase):
    id: int
    created_at: datetime.datetime

