
from db import Base, relationship
from sqlalchemy import Column, ForeignKey , VARCHAR, Integer, TIMESTAMP, Boolean



class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_date = Column(TIMESTAMP, nullable=False)
    status = Column(VARCHAR(20), nullable=False)
    tax_amount = Column(Integer, nullable=False)
    profit = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    shipping_address_id = Column(Integer, ForeignKey('address.id'))
    payment_method = Column(VARCHAR(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    #relationships
    user = relationship('User', back_populates='orders')
    payments = relationship('Payment', back_populates='order')
    order_items = relationship('OrderItem', back_populates='order')
    shipping_address = relationship("Address", back_populates="orders")


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    transaction_id = Column(VARCHAR(255), unique=True, nullable=False)
    status = Column(VARCHAR(20), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(VARCHAR)
    card_pan_masked = Column(VARCHAR(20))
    payment_date = Column(TIMESTAMP)
    #relationships
    order = relationship('Order', back_populates='payments')


class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP)
    #relationships
    user = relationship('User', back_populates='shopping_cart')
    product = relationship('Product', back_populates='shopping_cart')


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    #relationships
    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='orders')


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    street_address = Column(VARCHAR(255), nullable=False)
    city = Column(VARCHAR(100), nullable=False)
    state = Column(VARCHAR(100))
    postal_code = Column(VARCHAR(20))
    reciver_phone = Column(VARCHAR(11))
    reciver_fullname = Column(VARCHAR(50))
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP, nullable=True)
    #relationships
    user = relationship('User', back_populates='addresses')
    orders = relationship('Order', back_populates='shipping_address')