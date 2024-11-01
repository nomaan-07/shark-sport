from db import Base, relationship
from sqlalchemy import Column, ForeignKey , VARCHAR, Integer, TIMESTAMP, Boolean, LargeBinary
from tools import current_time

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(VARCHAR(300), nullable=False)
    subject = Column(VARCHAR(70), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  
    admin_id = Column(Integer, ForeignKey('admin.id'), nullable=True) 
    read_status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)
    user = relationship('User', back_populates='notifications')
    admin = relationship('Admin', back_populates='notifications')
