from fastapi import APIRouter, HTTPException, Request, Query,Form, File, UploadFile, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_db, Session, joinedload
from typing import Optional
from middleware.auth_middleware import create_access_token, auth_middleware, hash_pw, check_pw, PASSWORD_KEY, ALGORITH, get_current_user
from models.user import User as UserModel
from schemas.user import UserBase, UserCreate, UserUpdate, User, UserLogin, UserLoginResp, UserDeleteRequest
from schemas.message import UserLogoutMessage
from tools import BucketObj_2, current_time
from datetime import timedelta
import bcrypt, jwt


ACCESS_TOKEN_EXP = 3600000
REFRESH_TOKEN_EXP = 100


router = APIRouter(
    prefix="/api/user/Auth"
)

@router.post("/register", response_model=UserCreate, status_code=201)
def register_user(baseInfo: UserBase, db: Session=Depends(get_db)):
    """User registration / signup route"""
    if db.query(UserModel).filter(UserModel.username == baseInfo.username).first():
        raise HTTPException(status_code=409, detail="username exists")
    hashed_pw = hash_pw(baseInfo.password)
    new_user = UserModel(name=baseInfo.name, lastname=baseInfo.lastname, username=baseInfo.username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    return new_user


@router.post("/login", response_model=UserLoginResp, status_code=200)
def user_login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == credentials.username).first()
    if not db_user or not check_pw(credentials.password, db_user.password):
        raise HTTPException(status_code=400, detail="User with credentials not found")
    access_token = create_access_token(
        user_data={"uid": db_user.id,
                   "user_type": "user"},
        refresh=False
    )
    refresh_token = create_access_token(
        user_data={"uid": db_user.id,
                   "user_type": "user"},
        expiry=timedelta(days=REFRESH_TOKEN_EXP),
        refresh=True
    )
    db_user.access_token = access_token
    db_user.refresh_token = refresh_token
    db.commit()
    return {"access_token":access_token, "refresh_token":refresh_token, "token_type": "bearer"}



@router.post("/logout", response_model=UserLogoutMessage ,status_code=200)
def user_logout(db:Session=Depends(get_db), auth_dict=Depends(get_current_user)):
    """Requires Access Token of the current User to logout. Logout will wipe Access Token and Refresh Token"""
    if 'uid' not in auth_dict:
        raise HTTPException(status_code=400, detail="Invalid Token, logout faild")
    db_user = db.query(UserModel).filter(UserModel.id == auth_dict["uid"]).first()
    db_user.access_token = None
    db_user.refresh_token = None
    db.commit()
    return {"message": "logout succeed"}