from fastapi import APIRouter, HTTPException, status,Request, Query,Form, File, UploadFile, Depends, Response, Header
from fastapi.security.oauth2 import OAuth2PasswordBearer
from db import get_db, Session, joinedload
from typing import Optional
from middleware.auth_middleware import auth_middleware,auth_middleware, hash_pw, check_pw, create_access_token
from models.user import Admin as AdminModel
from schemas.user import AdminBase, AdminCreate, AdminLogin,AdminLoginResp
from tools import BucketObj_2, current_time
from datetime import timedelta
import bcrypt, jwt
from datetime import datetime



ACCESS_TOKEN_EXP = 3600
REFRESH_TOKEN_EXP = 1


router = APIRouter(
    prefix="/api/admin"
)




@router.post("/create_admin", response_model=AdminCreate, status_code=201)
def create_admin(admin_info:AdminBase, db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    if auth_dict["root_access"] == True:
        if db.query(AdminModel).filter(AdminModel.username == admin_info.username).first():
            raise HTTPException(status_code=409, detail="Admin Username already exsits")
        new_admin = AdminModel(
            name=admin_info.name,
            lastname=admin_info.lastname,
            username=admin_info.username,
            password=hash_pw(admin_info.password),
            email=admin_info.email,
            phone=admin_info.phone,
            root_access=admin_info.root_access,
            created_at=current_time()
        )
        db.add(new_admin)
        db.commit()
        return new_admin
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this route")


@router.post("/login", response_model=AdminLoginResp ,status_code=200)
def admin_login(credentials:AdminLogin, db:Session=Depends(get_db)):
    db_admin = db.query(AdminModel).filter(AdminModel.username == credentials.username).first()
    if not db_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if not check_pw(credentials.password, db_admin.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    access_token = create_access_token(
        user_data= {
            "uid": db_admin.id,
            "user_type": "admin",
            "root_access": db_admin.root_access
        },
        expiry=timedelta(seconds=ACCESS_TOKEN_EXP)
    )
    refresh_token = create_access_token(
        user_data= {
            "uid": db_admin.id,
            "user_type": "admin",
            "root_access": db_admin.root_access
        },
        expiry=timedelta(days=REFRESH_TOKEN_EXP),
        refresh=True
    )
    db_admin.access_token = access_token
    db_admin.refresh_key = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}



@router.get("/list_admins", status_code=200)
def list_admins(db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    return db.query(AdminModel).all()
