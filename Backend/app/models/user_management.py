from sqlalchemy import Column, Integer, String, Float, Text, Numeric, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


"""class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP)

    reviews = relationship("ProductReview", back_populates="user")
"""