from sqlalchemy import Column, Integer, Boolean, VARCHAR, ForeignKey, TIMESTAMP, LargeBinary
from sqlalchemy.orm import relationship
from db import Base

class Admin(Base):
    __tablename__ = 'admin'
    
    id = Column(VARCHAR(20), primary_key=True, index=True)
    name = Column(VARCHAR(50), nullable=False)
    lastname = Column(VARCHAR(50), nullable=False)
    username = Column(VARCHAR(100), unique=True, nullable=False)
    email = Column(VARCHAR(255), unique=True, nullable=False)
    phone = Column(VARCHAR(11))
    password = Column(LargeBinary)
    avatar_link = Column(VARCHAR, nullable=True)
    google_analytics_token = Column(VARCHAR, nullable=True)
    instagram_token = Column(VARCHAR, nullable=True)
    google_analyze_website = Column(VARCHAR, default=False)
    last_login = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP, default=None)
    root_access = Column(Boolean, default=False)

    # Define the relationship with Permission
    permissions = relationship("Permission", back_populates="admin")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    admin_id = Column(VARCHAR(20), ForeignKey("admin.id"), nullable=False)
    status = Column(Boolean, nullable=False)

    # Correctly reference the permissions relationship in Admin
    admin = relationship("Admin", back_populates="permissions")