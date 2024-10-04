from db import Base
from sqlalchemy import Column, Text, VARCHAR, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import relationship


class ProductCategory(Base):
    __tablename__ = "products_categories"

    id = Column(Text, primary_key=True)
    name = Column(Text, unique=True ,nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    products = relationship("Product", back_populates="category")
    



class Product(Base):
    __tablename__ = "products"


    id = Column(Text, primary_key=True)
    product_code = Column(Text, unique=True)
    name = Column(Text)
    description = Column(Text)
    category_id = Column(Text, ForeignKey('products_categories.id'))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    
    image_urls = relationship("Image", back_populates="product")
    category = relationship("ProductCategory", back_populates="products")
    attributes = relationship("ProductAttribute", back_populates="product")




class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    id = Column(Text, primary_key=True)
    product_id = Column(Text, ForeignKey('products.id'))
    price = Column(Text)
    offer_price = Column(Text)
    tags = Column(Text)
    brand = Column(Text)
    attributes = Column(Text)
    dimensions = Column(Text)
    weight = Column(Text)

    product = relationship("Product", back_populates="attributes")




class Image(Base):
    __tablename__ = "images"

    id = Column(Text, primary_key=True)
    url = Column(Text, nullable=False)
    product_code = Column(Text, ForeignKey("products.product_code"))
    created_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)


    product = relationship("Product", back_populates="image_urls")


class ProductInventory(Base):
    __tablename__ = "products_inventory"

    id = Column(Text, primary_key=True)
    quantity = Column(Integer)
    created_at= Column(TIMESTAMP)
    modified_at =Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
