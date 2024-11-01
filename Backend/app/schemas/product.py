from pydantic import BaseModel
import datetime
from typing import Annotated, List, Optional



class SpecificationModel(BaseModel):
    weight: Optional[str] = None
    fabric: Optional[str] = None

class SizeModel(BaseModel):
    size: str
    color: str
    quantity: int

class ProductBase(BaseModel):
    name: str
    description: str
    survey: str
    warranty: str
    brand: str
    category_id: int
    original_price: float

class CreateProductResponse(ProductBase):
    id: int
    price_after_discount: float
    discount_id: int
    created_at: datetime.datetime
    tags: List[int]
    specifications: List[SpecificationModel]
    sizes: List[SizeModel]
    images: List[str]




"""----------------------------------------discount Section----------------------------"""



class CategoryBase(BaseModel):
    name: str
    image_url: str
    description: Optional[str] = None


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


"""----------------------------------------Tag Section----------------------------"""



class TagBase(BaseModel):
    name: str

class Tag(TagBase):
    id: int