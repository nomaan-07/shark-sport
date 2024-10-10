"""from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, TEXT, LargeBinary, ForeignKey, VARCHAR, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), unique=True)
    description = Column(TEXT)
    survay = Column(TEXT)
    original_price = Column(TEXT)
    price_after_discount = Column(TEXT)
    warranty = Column(TEXT)
    size_id = Column(Integer, ForeignKey("size.id"))  # Assuming size_id is a VARCHAR, could be an Integer if it references sizes
    discount_id = Column(VARCHAR)  # Assuming discount_id is a VARCHAR, could be an Integer if it references discounts
    category_id = Column(VARCHAR)  # Assuming category_id is a VARCHAR, could be an Integer if it references categories
    specification_id = Column(VARCHAR)  # Assuming specification_id is a VARCHAR, could be an Integer if it references specifications
    brand = Column(TEXT)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    password = Column(LargeBinary)
    refresh_token = Column(LargeBinary)
    access_token = Column(LargeBinary)

    # Relationships
    size = relationship('Size', back_populates='products')
    category = relationship('ProductCategory', back_populates='products')
    specification = relationship('Specification', back_populates='products')
    tags = relationship('Tag', back_populates='product')
    images = relationship('ProductImage', back_populates='product')
    discount = relationship('Discount', back_populates='products')




class Size(Base):
    __tablename__ = 'size'

    id = Column(Integer, primary_key=True)
    product_type = Column(TEXT)
    sizes = Column(JSON)  
    colors = Column(JSON) 
    quantity = Column(Integer)

    # Relationship
    products = relationship('Product', back_populates='size')




class ProductCategory(Base):
    __tablename__ = 'product_category'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), unique=True)
    description = Column(TEXT)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    # Relationship
    products = relationship('Product', back_populates='category')




class Specification(Base):
    __tablename__ = 'specification'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    product_code = Column(VARCHAR, unique=True)
    description = Column(TEXT)

    # Relationship
    products = relationship('Product', back_populates='specification')




class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))
    product_id = Column(Integer, ForeignKey('products.id'))

    # Relationship
    product = relationship('Product', back_populates='tags')

class ProductImage(Base):
    __tablename__ = 'product_image'

    id = Column(Integer, primary_key=True)
    image_url = Column(TEXT)
    product_id = Column(Integer, ForeignKey('products.id'))

    # Relationship
    product = relationship('Product', back_populates='images')




class Discount(Base):
    __tablename__ = 'discount'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))
    discount_code = Column(VARCHAR(20), unique=True)
    discount_rate = Column(TEXT)
    created_at = Column(TIMESTAMP)
    expires_at = Column(TIMESTAMP)

    # Relationship
    products = relationship('Product', back_populates='discount')




class FavoritProduct(Base):
    __tablename__ = 'favorit_product'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)




class ProductReview(Base):
    __tablename__ = 'product_review'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer, ForeignKey('products.id'))
    name = Column(TEXT)
    points = Column(Integer)  # Assuming points range from 0 to 5
    description = Column(TEXT)
    Advantages = Column(JSON)  # Assuming JSON structure
    disAdvantages = Column(JSON)  # Assuming JSON structure
    created_at = Column(TIMESTAMP)
    status_id = Column(Integer)

    # Relationship
    product = relationship('Product', back_populates='reviews')
    status = relationship('ReviewStatus', back_populates='reviews')




class ReviewStatus(Base):
    __tablename__ = 'review_status'

    id = Column(Integer, primary_key=True)
    status = Column(TEXT)

    # Relationship
    reviews = relationship('ProductReview', back_populates='status')"""