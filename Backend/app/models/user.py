from db import Base
from sqlalchemy import Column, String, VARCHAR, TEXT, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = "users"

    id = Column(TEXT, primary_key=True)
    picture_url = Column(TEXT)
    username = Column(TEXT, nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(TEXT)
    phone = Column(TEXT)
    telephone = Column(TEXT)
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    password = Column(LargeBinary, nullable=False)

    addresses = relationship("Address", back_populates="user")




class Address(Base):
    __tablename__ = "user_addresses"

    id = Column(TEXT, primary_key=True)
    id_user = Column(TEXT, ForeignKey('users.id'))  # Corrected
    province = Column(VARCHAR)
    city = Column(VARCHAR)
    postal_code = Column(VARCHAR)
    detail = Column(TEXT)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    
    user = relationship("User", back_populates="addresses") 