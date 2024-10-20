from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from typing import Any

# Base Pydantic model for common fields
class BaseModelWithTimestamps(BaseModel):
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(description= "Unique name")
    description: Optional[str] = Field(default=None, description="Description about the product")
    survay: Optional[str] = None
    original_price: int
    warranty: Optional[str] = None
    discount_id: Optional[str] = None
    category_id: str = Field(description="Category must be a category id")
    brand: str

class ProductCreated(ProductBase):
    id: str 
    created_at: datetime
    price_after_discount: int
    
    

class ProductUpdate(ProductBase):
    id: str
    product_update: datetime
    price_after_discount: int
    

class Product(ProductCreated):
    modified_at: datetime
    deleted_at: datetime
    


# Size Schemas
class SizeBase(BaseModel):
    product_id: str
    size: Optional[Any] = None
    color: Optional[str] = None
    quantity: Optional[int] = None


class Size(SizeBase):
    modified_at: datetime
    id: str




   

# Product Category Schemas
class ProductCategoryBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class ProductCategoryCreate(ProductCategoryBase):
    created_at: datetime

class ProductCategoryUpdate(ProductCategoryBase):
    modified_at: datetime

class ProductCategoryDelete(ProductCategoryBase):
    deleted_at: datetime

class ProductCategory(ProductCategoryBase):
    created_at: datetime
    modified_at: datetime
    deleted_at: datetime



# Discount
class DiscountBase(BaseModel):
    name: str
    discount_code: str = Field(max_length=10)
    discount_rate: int = Field(ge=0, le=100, description="percentage 0-100%")
    expires_at : datetime

class Discount(DiscountBase):
    id: str
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class ProductReviewBase(BaseModel):
    name: str
    points: int
    description: str
    advantages: Optional[list[str]] = []
    disadvantages: Optional[list[str]] = []

class ProductReviewCreate(ProductReviewBase):
    product_id: str
    user_id: str

class ProductReviewUpdate(ProductReviewBase):
    pass

class ProductReview(ProductReviewBase):
    id: str
    product_id: str
    user_id: str
    created_at: str
    status_id: int


class ProductTags(BaseModel):
    product_id: str
    tag_names: List[str]



class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class Tag(TagBase):
    id: str





class SpecificationBase(BaseModel):
    name: str
    description: str


class SpecificationCreated(SpecificationBase):
    id: str
    product_id: str
    