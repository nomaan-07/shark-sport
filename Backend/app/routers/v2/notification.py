from fastapi import APIRouter, HTTPException, Request, Query,Form, File, UploadFile, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordBearer
from db import get_db, Session, joinedload
from typing import Optional
from middleware.auth_middleware import auth_middleware
from models.user import User as UserModel
from schemas.notification import Notification
from tools import BucketObj_2, current_time
from datetime import timedelta
from models.notification import Notification as NotificationModel 

router = APIRouter (
    prefix="/api/notification"
)
   

@router.get("/user/get/list{limit}{skip}", response_model=Notification,status_code=200)
def list_admin_notifications(index: bool = True, limit: int = 10, skip: int = 0, db: Session = Depends(get_db), auth_dict = Depends(auth_middleware)):
    query_notifs = db.query(NotificationModel).filter(NotificationModel.user_id == auth_dict["uid"])
    if index:
        query_notifs = query_notifs.order_by(NotificationModel.created_at.desc())
    query_notifs = query_notifs.offset(skip).limit(limit)
    return query_notifs.all()


@router.get("/admin/get/list{limit}{skip}", response_model=Notification, status_code=200)
def list_admin_notifications(index: bool = True, limit: int = 10, skip: int = 0, db: Session = Depends(get_db), auth_dict = Depends(auth_middleware)):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    query_notifs = db.query(NotificationModel).filter(NotificationModel.admin_id == auth_dict["uid"])
    if index:
        query_notifs = query_notifs.order_by(NotificationModel.created_at.desc())
    query_notifs = query_notifs.offset(skip).limit(limit)
    return query_notifs.all()



@router.get("all_users/get/{notification_id}", response_model=Notification, status_code=200)
def read_notification(notification_id: int, db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    db_notific = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if db_notific:
        return db_notific
    raise HTTPException(status_code=404, detail=f"Notification with id {notification_id} not found")

