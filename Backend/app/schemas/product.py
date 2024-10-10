from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from typing import Any

# Base Pydantic model for common fields
class BaseModelWithTimestamps(BaseModel):
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    survay: Optional[str] = None
    original_price: str
    price_after_discount: str
    warranty: Optional[str] = None
    size_id: Optional[str] = None
    discount_id: Optional[str] = None
    category_id: Optional[str] = None
    specification_id: Optional[str] = None
    tags: List[str] = []
    brand: str

class ProductCreate(ProductBase):
    id: int
    created_at: datetime
    
    

class ProductUpdate(ProductBase):
    id: int
    product_update: datetime

class Product(ProductBase):
    id: int
    created_at: datetime
    modified_at: datetime
    deleted_at: datetime
    


# Size Schemas
class SizeBase(BaseModel):
    product_type: Optional[str] = None
    sizes: Optional[Any] = None
    colors: Optional[Any] = None
    quantity: Optional[int] = None

class SizeCreate(SizeBase):
    pass

class SizeUpdate(SizeBase):
    pass

class Size(SizeBase, BaseModelWithTimestamps):
    id: int

   

# Product Category Schemas
class ProductCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryUpdate(ProductCategoryBase):
    pass

class ProductCategory(ProductCategoryBase, BaseModelWithTimestamps):
    id: int

# Specification Schemas
class SpecificationBase(BaseModel):
    name: str
    product_code: str
    description: Optional[str] = None

class SpecificationCreate(SpecificationBase):
    pass

class SpecificationUpdate(SpecificationBase):
    pass

class Specification(SpecificationBase):
    id: int

    

# Tag Schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class Tag(TagBase):
    id: int

    

# Product Image Schemas
class ProductImageBase(BaseModel):
    image_url: str
    product_id: int

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageUpdate(ProductImageBase):
    pass

class ProductImage(ProductImageBase):
    id: int

    

# Discount Schemas
class DiscountBase(BaseModel):
    name: str
    discount_code: str
    discount_rate: str

class DiscountCreate(DiscountBase):
    pass

class DiscountUpdate(DiscountBase):
    pass

class Discount(DiscountBase):
    id: int

   

# Favorite Product Schemas
class FavoritProductBase(BaseModel):
    product_id: int
    user_id: int

class FavoritProductCreate(FavoritProductBase):
    pass

class FavoritProductUpdate(FavoritProductBase):
    pass

class FavoritProduct(FavoritProductBase):
    id: int

    

# Product Review Schemas
class ProductReviewBase(BaseModel):
    user_id: int
    product_id: int
    name: Optional[str] = None
    points: int
    description: Optional[str] = None
    Advantages: Optional[Any] = None
    disAdvantages: Optional[Any] = None
    status_id: Optional[int] = None

class ProductReviewCreate(ProductReviewBase):
    pass

class ProductReviewUpdate(ProductReviewBase):
    pass

class ProductReview(ProductReviewBase):
    id: int



# Review Status Schemas
class ReviewStatusBase(BaseModel):
    status: str

class ReviewStatusCreate(ReviewStatusBase):
    pass

class ReviewStatusUpdate(ReviewStatusBase):
    pass

class ReviewStatus(ReviewStatusBase):
    id: int

    