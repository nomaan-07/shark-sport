from db import Base
from sqlalchemy import Column, String, VARCHAR, TEXT, LargeBinary
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

class UserDB(Base):
    __tablename__ = "users"

    id = Column(TEXT, primary_key=True)
    username = Column(TEXT, nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(TEXT)
    phone = Column(TEXT)
    telephone = Column(TEXT)
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    password = Column(LargeBinary, nullable=False)
