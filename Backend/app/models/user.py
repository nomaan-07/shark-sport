from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, TIMESTAMP, TEXT, Integer, VARCHAR, Boolean, LargeBinary


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    lastname = Column(VARCHAR(100), nullable=False)
    username = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(255))
    phone_number = Column(VARCHAR(10))
    password = Column(LargeBinary, nullable=False)
    avatar_link = Column(TEXT)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
