from fastapi import APIRouter, HTTPException, Request, Depends, Response
from db import get_db, Session, joinedload
from middleware.auth_middleware import create_access_token, user_auth_middleware, hash_pw, check_pw
from models.user import User as UserModel
from schemas.user import UserBase, UserCreate, UserUpdate, User, UserLogin, UserLoginResp
from tools import BucketObj, current_time
from datetime import timedelta
import bcrypt
router = APIRouter(
    prefix="/api/user"
)

ACCESS_TOKEN_EXP = 3600
REFRESH_TOKEN_EXP = 2



@router.post("/register", response_model=UserCreate, status_code=201)
def register_user(baseInfo: UserBase, db: Session=Depends(get_db)):
    """User registration / signup route"""
    if db.query(UserModel).filter(UserModel.username == baseInfo.username).first():
        raise HTTPException(status_code=409, detail="username exists")
    hashed_pw = bcrypt.hashpw(baseInfo.password.encode(), bcrypt.gensalt()).decode()
    new_user = UserModel(name=baseInfo.name, lastname=baseInfo.lastname, username=baseInfo.username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    return new_user


@router.post("/login", response_model=UserLoginResp, status_code=200)
def user_login(credentials: UserLogin, response:Response, db: Session = Depends(get_db)):
    user_db = db.query(UserModel).filter(
        UserModel.username == credentials.username
    ).first()
    
    if not user_db or not bcrypt.checkpw(credentials.password.encode(), user_db.password.encode()):
        raise HTTPException(status_code=404, detail="User with credentials not found")
    
    access_token = create_access_token(
        user_data={"uid": user_db.id},
        refresh=False
    )
    
    refresh_token = create_access_token(
        user_data={"uid": user_db.id},
        expiry=timedelta(days=REFRESH_TOKEN_EXP),
        refresh=True
    )
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite='Lax')
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite='Lax')

    return UserLoginResp(access_token=access_token)