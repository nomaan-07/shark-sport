from fastapi import APIRouter, HTTPException, Request, Query,Form, File, UploadFile, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordBearer
from db import get_db, Session, joinedload
from typing import Optional
from middleware.auth_middleware import create_access_token, auth_middleware, hash_pw, check_pw, PASSWORD_KEY, ALGORITH, get_current_user
from models.user import User as UserModel
from schemas.user import UserBase, UserCreate, UserUpdate, User, UserLogin, UserLoginResp, UserDeleteRequest
from schemas.message import UserLogoutMessage
from tools import BucketObj_2, current_time
from datetime import timedelta
import bcrypt, jwt


router = APIRouter(
    prefix="/api/user"
)
router_admin_user = APIRouter(
    prefix="/api/admin/user-management"
)

token_router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


ACCESS_TOKEN_EXP = 3600
REFRESH_TOKEN_EXP = 1



@router.post("/test/")
def test(token=Depends(get_current_user)):
    return token


@token_router.post("/token")
def refresh_token(db:Session=Depends(get_db),refresh_token=Depends(oauth_scheme)):
    try:
        verified_token = jwt.decode(refresh_token, PASSWORD_KEY, [ALGORITH])
        if verified_token["refresh"]:
            uid = verified_token["user"]["uid"]
            new_access_token = create_access_token(
            user_data={"uid": uid},
            refresh=False
            )
            db_user = db.query(UserModel).filter(UserModel.id == uid).first()
            db_user.access_token = new_access_token
            db.commit()
            return {"access_token": new_access_token, "token_type": "bearer"}
        raise HTTPException(status_code=400, detail="Refresh token needed")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token is expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")




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


@router.get("/list_users", response_model=list, status_code=200)
def list_users(
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


@router.get("/users/{user_id}", response_model=User, status_code=200)
def read_user(user_id: int, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return 



@router.delete("/users", status_code=200)
def delete_users(request: UserDeleteRequest, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    users_to_delete = db.query(UserModel).filter(UserModel.id.in_(request.user_ids)).all()
    if not users_to_delete:
        raise HTTPException(status_code=404, detail="No users found for the provided IDs")
    
    del_users = []
    for user in users_to_delete:
        user.deleted_at = current_time()
        del_users.append(user)
    
    db.commit()
    return del_users

