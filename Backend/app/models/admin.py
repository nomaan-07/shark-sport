from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db import Base

class Admin(Base):
    __tablename__ = 'admin'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(11))
    password = Column(String)
    avatar_link = Column(String, nullable=True)
    google_analytics_token = Column(String, nullable=True)
    instagram_token = Column(String, nullable=True)
    google_analyze_website = Column(Boolean, default=False)
    last_login = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    root_access = Column(Boolean, default=False)

    # Define the relationship with Permission
    permissions = relationship("Permission", back_populates="admin")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False)
    status = Column(Boolean, nullable=False)

    # Correctly reference the permissions relationship in Admin
    admin = relationship("Admin", back_populates="permissions")