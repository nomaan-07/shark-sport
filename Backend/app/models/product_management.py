from sqlalchemy import Column, Integer, String, Float, Text, Numeric, JSON, TIMESTAMP, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Base




class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    code = Column(String(50), nullable=False, unique=True)
    """category_id = Column(Text, ForeignKey("categories.id"))"""
    weight = Column(VARCHAR(50), nullable=False)
    fabric_type = Column(String(50), nullable=False)
    pattern = Column(VARCHAR(50), nullable=False)
    color = Column(VARCHAR(50), nullable=False)
    size_options = Column(JSON, nullable=False)  #  ['L', 'M', 'S', 'XS']
    price = Column(Integer, nullable=False)
    seller_id = Column(VARCHAR)
    image_urls = Column(JSON)
    rating = Column(Float, default=0)
    reviews_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    """category = relationship("Category", back_populates="product")"""
    


"""class Category(Base):
    __tablename__ = "categories"

    id = Column(Text, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)

    product = relationship("Product", back_populates="category")


class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Text, primary_key=True)
    name = Column(VARCHAR(255))
    item_id =Column(Text, ForeignKey())
    created_at = Column(TIMESTAMP)
    expires_at = Column()

    item = relationship("Product", back_populates="")"""