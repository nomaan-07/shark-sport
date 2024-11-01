from fastapi import APIRouter, HTTPException, Request, Query,Form, File, UploadFile, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordBearer
from db import get_db, Session, joinedload
from typing import Optional
from middleware.auth_middleware import create_access_token, auth_middleware, hash_pw, check_pw, PASSWORD_KEY, ALGORITH, get_current_user
from models.user import User as UserModel
from models.user import Admin as AdminModel
from schemas.user import UserBase, UserCreate, UserUpdate, User, UserLogin, UserLoginResp, UserDeleteRequest
from schemas.message import UserLogoutMessage, UserGetMessage
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


from typing import Annotated

@router.get("/get_me",response_model=UserGetMessage ,status_code=200)
def get_current_user(db: Session=Depends(get_db), auth_dict = Depends(auth_middleware)):
    db_user = db.query(UserModel).filter(UserModel.id == auth_dict["uid"]).first()
    response = {"auth_dict": auth_dict, 
                "user": {
                    "name": db_user.name,
                    "lastname": db_user.lastname,
                    "username": db_user.username,
                    "email": db_user.email,
                    "phone": db_user.phone_number,
                    "avatar_url": db_user.avatar_link,
                    }
                }
    return response



@router.put("/users/{user_id}", response_model=User, status_code=200)
def update_user(
    name: str = Form(...),
    lastname: str = Form(...),
    username: str = Form(...),
    email: str = Form(default=None),
    phone_number: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile| None = File(default=None),
    db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)
    ):
    db_user = db.query(UserModel).filter(UserModel.id == auth_dict["uid"]).first()
    if not db_user :
        raise HTTPException(status_code=400, detail="User not found")
    if auth_dict["user_type"] == "admin":
        raise HTTPException(status_code=400, detail="only Users can modifiy this information")
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
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


from pydantic import BaseModel
class UserDeleteRequest(BaseModel):
    usernames: list[str]

@router_admin_user.delete("/list/delete_users_admins", status_code=200)
def delete_users(users_request: UserDeleteRequest, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    """root accessed admins also can delete admins"""
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    usernames = users_request.usernames
    
    if not usernames:
        raise HTTPException(status_code=400, detail="Usernames list cannot be empty")

    del_users = []

    if auth_dict["root_access"] == True:
        # Delete both users and admins by username
        users_to_delete = db.query(UserModel).filter(UserModel.username.in_(usernames)).all()
        admins_to_delete = db.query(AdminModel).filter(AdminModel.username.in_(usernames)).all()

        if not users_to_delete and not admins_to_delete:
            raise HTTPException(status_code=404, detail="No users or admins found for the provided usernames")

        for user in users_to_delete:
            user.deleted_at = current_time()
            del_users.append({"role": "user", "id": user.id, "username": user.username})
            db.delete(user)

        for admin in admins_to_delete:
            admin.deleted_at = current_time()
            del_users.append({"role": "admin", "id": admin.id, "username": admin.username})
            db.delete(admin)
    else:
        # Delete only users by username
        users_to_delete = db.query(UserModel).filter(UserModel.username.in_(usernames)).all()

        if not users_to_delete:
            raise HTTPException(status_code=404, detail="No users found for the provided usernames")

        for user in users_to_delete:
            user.deleted_at = current_time()
            del_users.append({"role": "user", "id": user.id, "username": user.username})
            db.delete(user)

    db.commit()

    return {"deleted_users": del_users}




@router_admin_user.get("/list_all", status_code=200)
def list_all_users(admins: bool = False, users: bool = False, index: bool = True, limit: int = 10, skip: int = 0, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    response = []
    if admins == False and users == False:
        raise HTTPException(status_code=400, detail="Atleast one of the admins or users most be true")
    if admins:

        admin_query = db.query(AdminModel).offset(skip).limit(limit).all()
        for admin in admin_query:
            response.append({
                "role": "admin",
                "phone": admin.phone,
                "email": admin.email,
                "name": admin.name,
                "lastname": admin.lastname,
                "username": admin.username,
                "avatar_link": admin.avatar_link,
                "root_access":admin.root_access
            })
        limit -= len(admin_query)

    if users:
        user_query = db.query(UserModel).offset(skip).limit(limit).all()
        for user in user_query:
            response.append({
                "role": "user",
                "phone": user.phone_number,
                "email": user.email,
                "name": user.name,
                "lastname": user.lastname,
                "username": user.username,
                "avatar_link": user.avatar_link
            })
    
    total = len(response)
    return {"sender_root_access":auth_dict["root_access"],"total": total, "results": response}


