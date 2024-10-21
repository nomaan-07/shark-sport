from db import Base, relationship
from sqlalchemy import Column, ForeignKey , JSON, VARCHAR, Integer, TIMESTAMP, Boolean



class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), unique=True)
    description = Column(VARCHAR(255))
    survey = Column(VARCHAR(5000))
    original_price = Column(Integer)
    price_after_discount = Column(Integer)
    warranty = Column(VARCHAR(100))
    discount_id = Column(Integer, ForeignKey('discount.id'))
    category_id = Column(Integer, ForeignKey('product_category.id'))
    brand = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    #relationships
    category = relationship("ProductCategory", back_populates="products")
    discount = relationship("Discount", back_populates="products")
    reviews = relationship('ProductReview', back_populates='product')
    images = relationship('ProductImage', back_populates='product')
    tags = relationship('ProductTag', back_populates='product')
    sizes = relationship('Size', back_populates='product')
    specifications = relationship('Specification', back_populates='product')
    orders = relationship('OrderItem', back_populates='product')
    shopping_cart = relationship('ShoppingCart', back_populates='product')
    favorit_products = relationship('FavoritProduct', back_populates='product')
    compare_list = relationship('CompareList', back_populates='product')


class ProductCategory(Base):
    __tablename__ = 'product_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(VARCHAR(300))
    name = Column(VARCHAR(255), unique=True)
    description = Column(VARCHAR(100))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP, nullable=True)
    #relationships
    products = relationship('Product', back_populates='category')

class ProductReview(Base):
    __tablename__ = 'product_review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    name = Column(VARCHAR)
    points = Column(Integer)
    description = Column(VARCHAR(500))
    advantages = Column(JSON)
    disadvantages = Column(JSON)
    created_at = Column(TIMESTAMP)
    status = Column(VARCHAR(10))
    #relationships
    user = relationship('User', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')


class ProductImage(Base):
    __tablename__ = 'product_image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(VARCHAR(300))
    product_id = Column(Integer, ForeignKey('products.id'))
    #relationships
    product = relationship('Product', back_populates='images')


class FavoritProduct(Base):
    __tablename__ = 'favorit_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    #relationships
    user = relationship('User', back_populates='favorit_products')
    product = relationship('Product', back_populates='favorit_products')


class Size(Base):
    __tablename__ = 'size'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    size = Column(VARCHAR(10))
    color = Column(VARCHAR(50))
    quantity = Column(Integer)
    modified_at = Column(TIMESTAMP)
    #relationships
    product = relationship('Product', back_populates='sizes')


class Specification(Base):
    __tablename__ = 'specification'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255))
    product_id = Column(Integer, ForeignKey('products.id'))
    description = Column(VARCHAR(300))
    #relationships
    product = relationship('Product', back_populates='specifications')


class Discount(Base):
    __tablename__ = 'discount'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100))
    discount_code = Column(VARCHAR(20), unique=True)
    discount_rate = Column(Integer)
    created_at = Column(TIMESTAMP, nullable=False)
    expires_at = Column(TIMESTAMP,)
    #relationships
    products = relationship('Product', back_populates='discount')


class CompareList(Base):
    __tablename__ = 'compare_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    #relationships
    user = relationship('User', back_populates='compare_list')
    product = relationship('Product', back_populates='compare_list')