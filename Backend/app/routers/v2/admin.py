from fastapi import APIRouter, HTTPException, status,Request, Query,Form, File, UploadFile, Depends, Response, Header
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_db, Session, joinedload
from typing import Optional
from middleware.auth_middleware import auth_middleware,auth_middleware, hash_pw, check_pw, create_access_token
from models.user import Admin as AdminModel
from schemas.user import AdminBase, AdminCreate, AdminLogin,AdminLoginResp
from tools import BucketObj_2, current_time
from datetime import timedelta
from datetime import datetime
from schemas.message import AdminGetMe



ACCESS_TOKEN_EXP = 360000
REFRESH_TOKEN_EXP = 100


router = APIRouter(
    prefix="/api/admin"
)




@router.post("/create_admin", response_model=AdminCreate, status_code=201)
def create_admin(avatar:UploadFile=File(...),
                 name:str= Form(...),
                 lastname:str= Form(...),
                 username:str= Form(...),
                 password:str= Form(...),
                 email:str= Form(...),
                 phone:str= Form(...),
                 root_access:bool=Form(...),
                 db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    if auth_dict["root_access"] == True:
        if db.query(AdminModel).filter(AdminModel.username == username).first():
            raise HTTPException(status_code=409, detail="Admin Username already exsits")
        if db.query(AdminModel).filter(AdminModel.email == email).first():
            raise HTTPException(status_code=409, detail="Email Already exists")
        avatar_obj = BucketObj_2([avatar], [username], "image/profiles")
        avatar_obj.upload_images()
        avatar_link = avatar_obj.perma_links[0]
        new_admin = AdminModel(
            name=name,
            lastname=lastname,
            username=username,
            password=hash_pw(password),
            email=email,
            phone=phone,
            root_access=root_access,
            avatar_link = avatar_link,
            created_at=current_time()
        )
        db.add(new_admin)
        db.commit()
        return new_admin
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied, required root access")


@router.post("/login", response_model=AdminLoginResp ,status_code=200)
def admin_login(credentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    db_admin = db.query(AdminModel).filter(AdminModel.username == credentials.username).first()
    if not db_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password or username invalid")
    if not check_pw(credentials.password, db_admin.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password or username invalid")
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
    db_admin.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type":"bearer"}



@router.get("/list_admins", status_code=200)
def list_admins(db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    return db.query(AdminModel).all()


@router.get("/get_me", response_model=AdminGetMe, status_code=200)
def admin_get_me(db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    db_admin = db.query(AdminModel).filter(AdminModel.id == auth_dict["uid"]).first()
    admin_get_me_dict = {"auth_dict": {
                            "uid": auth_dict["uid"],
                            "user_type": auth_dict["user_type"],
                            "refresh": auth_dict["refresh"], 
                            "root_access": auth_dict["root_access"] 
                            },
                        "admin": {
                            "name": db_admin.name,
                            "lastname": db_admin.lastname, 
                            "username": db_admin.username, 
                            "email": db_admin.email,
                            "phone": db_admin.phone,
                            "avatar_url": db_admin.avatar_link,
                            "google_analytics_token": db_admin.google_analytics_token,
                            "instagram_token": db_admin.instagram_token,
                            "google_analyze_website": db_admin.google_analytics_token,
                            "last_login":db_admin.last_login, 
                            "created_at": db_admin.created_at, 
                            "modified_at": db_admin.modified_at,
                            "deleted_at": db_admin.deleted_at
                            }
                        }
    return admin_get_me_dict

from schemas.user import AdminUpdateResp
@router.put("/update/",response_model=AdminUpdateResp, status_code=200)
def update_admin(avatar:UploadFile=File(...),
                 name:str= Form(...),
                 lastname:str= Form(...),
                 username:str= Form(...),
                 password:str= Form(...),
                 email:str= Form(...),
                 phone:str= Form(...),
                 root_access:bool=Form(...),
                 google_analyze_website:bool=Form(...),
                 google_analytics_token:str=Form(...),
                 instagram_token:str=Form(...),
                 db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    db_admin = db.query(AdminModel).filter(AdminModel.id==auth_dict["uid"]).first()
    new_avatar_url = BucketObj_2([avatar],[name],"images/profiles")
    new_avatar_url.upload_images()
    db_admin.name = name
    db_admin.lastname = lastname
    db_admin.username=username
    db_admin.password=hash_pw(password)
    db_admin.email=email
    db_admin.phone=phone
    db_admin.root_access=root_access
    db_admin.google_analytics_token=google_analytics_token
    db_admin.google_analyze_website=google_analyze_website
    db_admin.instagram_token=instagram_token
    db.commit()
    return db_admin