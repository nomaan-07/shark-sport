from fastapi import APIRouter, HTTPException, Request, Query,Form, File, UploadFile, Depends, Response
from db import get_db, Session, joinedload
from typing import Optional
from middleware.auth_middleware import create_access_token, user_auth_middleware, hash_pw, check_pw
from models.user import User as UserModel
from schemas.user import UserBase, UserCreate, UserUpdate, User, UserLogin, UserLoginResp, UserDeleteRequest
from tools import BucketObj_2, current_time
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
    """response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite='Lax')
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite='Lax')"""

    return {"access_token":access_token, "refresh_token":refresh_token}



@router.put("/users/{user_id}", response_model=User, status_code=200)
def update_user(
    user_id: int,
    name: str = Form(...),
    lastname: str = Form(...),
    username: str = Form(...),
    email: str = Form(default=None),
    phone_number: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile| None = File(default=None),
    db: Session = Depends(get_db)
    ):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = name
    db_user.lastname = lastname
    db_user.username = username
    db_user.email = email
    db_user.phone_number = phone_number
    db_user.password = password
    if avatar:
        avatar_url = BucketObj_2(avatar, [f"{db_user.id}"], "/avatars").perma_links
        db_user.avatar_url = avatar_url[0]
    db_user.modified_at = current_time()
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users")
def read_users(
    show_deleted: bool = Query(False),
    limit: int = Query(10),
    skip: int = Query(0),
    db: Session = Depends(get_db)
    ):
    query = db.query(UserModel)
    if not show_deleted:
        query = query.filter(UserModel.deleted_at == None)
    users = query.offset(skip).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return 



@router.delete("/users", status_code=200)
def delete_users(request: UserDeleteRequest, db: Session = Depends(get_db)):
    users_to_delete = db.query(UserModel).filter(UserModel.id.in_(request.user_ids)).all()
    if not users_to_delete:
        raise HTTPException(status_code=404, detail="No users found for the provided IDs")
    
    del_users = []
    for user in users_to_delete:
        user.deleted_at = current_time()
        del_users.append(user)
    
    db.commit()
    return del_users