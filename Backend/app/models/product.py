from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, TEXT, LargeBinary, ForeignKey, VARCHAR, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON


class Product(Base):
    __tablename__ = 'products'

    id = Column(VARCHAR(255), primary_key=True)
    name = Column(VARCHAR(255), unique=True)
    description = Column(VARCHAR(300))
    survay = Column(VARCHAR(2000))
    original_price = Column(Integer, nullable=False)
    price_after_discount = Column(Integer)
    warranty = Column(VARCHAR(255))
    discount_id = Column(VARCHAR(100), ForeignKey("discount.discount_code"))  # Assuming discount_id is a VARCHAR, could be an Integer if it references discounts
    category_id = Column(VARCHAR(255), ForeignKey("product_category.id"))  # Assuming category_id is a VARCHAR, could be an Integer if it references categories
    brand = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)



    # Relationships
    sizes = relationship("Size", back_populates="product")
    category = relationship("ProductCategory", back_populates="product")
    discount = relationship("Discount", back_populates="products")
    reviews = relationship("ProductReview", back_populates="product")
    favorit_products = relationship("FavoritProduct", back_populates="product")
    specifications = relationship("Specification", back_populates="product")
    tags = relationship("ProductTag", back_populates="product")
    image = relationship("Image", back_populates="product")




class Image(Base):
    __tablename__ = "product_images"

    id = Column(VARCHAR, primary_key=True)
    product_id = Column(VARCHAR(255), ForeignKey("products.id"))
    url = Column(VARCHAR(300))

    product = relationship("Product", back_populates="image")


class Size(Base):
    __tablename__ = 'size'

    id = Column(VARCHAR, primary_key=True)
    product_id = Column(VARCHAR(300), ForeignKey("products.id"))
    size = Column(VARCHAR(10))  
    color = Column(VARCHAR) 
    quantity = Column(Integer)
    modified_at = Column(TIMESTAMP)
    # Relationship
    product = relationship("Product", back_populates="sizes")




class ProductCategory(Base):
    __tablename__ = 'product_category'

    id = Column(VARCHAR(300), primary_key=True)
    name = Column(VARCHAR(255), unique=True)
    description = Column(VARCHAR(600))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    # Relationship
    product = relationship("Product", back_populates="category")




class Discount(Base):
    __tablename__ = 'discount'

    id = Column(VARCHAR(300), primary_key=True)
    name = Column(VARCHAR(100))
    discount_code = Column(VARCHAR(20), unique=True)
    discount_rate = Column(Integer)
    expires_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    # Relationship
    products = relationship("Product", back_populates="discount")



class ProductReview(Base):
    __tablename__ = 'product_review'

    id = Column(VARCHAR(300), primary_key=True)
    user_id = Column(VARCHAR(300))
    product_id = Column(VARCHAR(300), ForeignKey("products.id"))
    name = Column(TEXT)
    points = Column(Integer)  # 0-5 rating
    description = Column(TEXT)
    advantages = Column(JSON)
    disadvantages = Column(JSON)
    created_at = Column(TIMESTAMP)
    status_id = Column(Integer, ForeignKey("review_status.id"))
    # Relationship
    product = relationship("Product", back_populates="reviews")
    status = relationship("ReviewStatus", back_populates="reviews")



class ReviewStatus(Base):
    __tablename__ = 'review_status'

    id = Column(Integer, primary_key=True)
    status = Column(TEXT)
    # Relationship
    reviews = relationship("ProductReview", back_populates="status")


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))



class ProductTag(Base):
    __tablename__ = 'productTag'

    product_id = Column(TEXT, ForeignKey("products.id"), primary_key=True)
    tag_id = Column(TEXT, ForeignKey("tag.id"), primary_key=True)
    # Relationship
    product = relationship("Product", back_populates="tags")
    tag = relationship("Tag")

class FavoritProduct(Base):
    __tablename__ = 'favorit_product'

    id = Column(VARCHAR(300), primary_key=True)
    product_id = Column(VARCHAR(300), ForeignKey("products.id"))
    user_id = Column(VARCHAR(300))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    # Relationship
    product = relationship("Product", back_populates="favorit_products")

class Specification(Base):
    __tablename__ = 'specification'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    product_id = Column(VARCHAR(300), ForeignKey("products.id"), unique=True)
    description = Column(TEXT)
    # Relationship
    product = relationship("Product", back_populates="specifications")