from db import Base, relationship
from sqlalchemy import Column, ForeignKey , VARCHAR, Integer, TIMESTAMP, Boolean, LargeBinary
from tools import current_time


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    lastname = Column(VARCHAR(50), nullable=False)
    username = Column(VARCHAR(100), unique=True, nullable=False)
    access_token = Column(VARCHAR(500))
    refresh_token = Column(VARCHAR(500))
    email = Column(VARCHAR(255), unique=True, nullable=False)
    phone = Column(VARCHAR(11))
    password = Column(LargeBinary, nullable=False)
    avatar_link = Column(VARCHAR(300))
    google_analytics_token = Column(VARCHAR)
    instagram_token = Column(VARCHAR)
    google_analyze_website = Column(VARCHAR, default=False)
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP, nullable=True, default=None)
    root_access = Column(Boolean, default=False)
    #relationships
    permissions = relationship('Permission', back_populates='admin')


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.id'), nullable=False)
    status = Column(Boolean, nullable=False)
    #relationships
    admin = relationship('Admin', back_populates='permissions')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False)
    lastname = Column(VARCHAR(25), nullable=False)
    username = Column(VARCHAR(35), nullable=False, unique=True)
    access_token = Column(VARCHAR(500))
    refresh_token = Column(VARCHAR(500))
    email = Column(VARCHAR(255))
    phone_number = Column(VARCHAR(10))
    password = Column(LargeBinary, nullable=False)
    avatar_link = Column(VARCHAR(300))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    #relationships
    reviews = relationship('ProductReview', back_populates='user')
    favorit_products = relationship('FavoritProduct', back_populates='user')
    addresses = relationship('Address', back_populates='user')
    orders = relationship('Order', back_populates='user')
    shopping_cart = relationship('ShoppingCart', back_populates='user')
    tickets = relationship('Ticket', back_populates='user')
    comments = relationship('TicketComment', back_populates='user')
    favorite_articles = relationship('UserFavoriteArticle', back_populates='user')
    compare_list = relationship('CompareList', back_populates='user')

    def __init__(self, name: str, lastname:str , username: str, password: str,email=None, phone_number=None, avatar_link=None):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.avatar_link = avatar_link
        self.created_at = current_time()


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subject = Column(VARCHAR(255), nullable=False)
    thumbnail_url = Column(VARCHAR(300))
    description = Column(VARCHAR(1000))
    status = Column(VARCHAR(50), nullable=False)
    priority = Column(VARCHAR(50))
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    resolved_at = Column(TIMESTAMP)
    #relationships
    user = relationship('User', back_populates='tickets')
    comments = relationship('TicketComment', back_populates='ticket')


class TicketComment(Base):
    __tablename__ = 'ticket_comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(VARCHAR(1000))
    created_at = Column(TIMESTAMP, nullable=False)
    #relationships
    user = relationship('User', back_populates='comments')
    ticket = relationship('Ticket', back_populates='comments')