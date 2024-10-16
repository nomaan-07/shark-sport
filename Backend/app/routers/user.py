from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from models import user as ModelUser
from schemas import user as SchemaUser
from db import get_db, Session
from datetime import timedelta
import jwt, bcrypt
from tools import current_time
from tools import BucketObj
from middleware.auth_middleware import user_auth_middleware, admin_auth_middleware,create_access_token, decode_token

REFRESH_TOKEN_EXPIRY = 2

router = APIRouter(
    prefix="/user"
)

admin_router = APIRouter(
    prefix="/admin"
)


@router.post("/create", response_model=SchemaUser.UserCreateResp, status_code=201)
def signup(credentials: SchemaUser.UserBase, db: Session=Depends(get_db)):

    if not db.query(ModelUser.User).filter(ModelUser.User.username == credentials.username).first():

        hashed_pw = bcrypt.hashpw(password=credentials.password.encode(), salt=bcrypt.gensalt())
        new_user = ModelUser.User(name=credentials.name,
                                lastname=credentials.lastname,
                                username=credentials.username,
                                password=hashed_pw,
                                created_at=current_time()
                                )
        db.add(new_user)
        db.commit()
        return new_user
    raise HTTPException(status_code=409, detail="duplicated user")



@router.post("/login",response_model=SchemaUser.LoginResp ,status_code=200)
def login(credentials: SchemaUser.Login, db: Session=Depends(get_db)):
    user_db = db.query(ModelUser.User).filter(ModelUser.User.username == credentials.username).first()

    if user_db:
        check_hash_pw = bcrypt.checkpw(credentials.password.encode(), user_db.password)

        if check_hash_pw:
            access_token = create_access_token(
            user_data={
                'uid': user_db.id
            })
            refresh_token = create_access_token(
                user_data= {
                    'username': user_db.username,
                    'uid': user_db.id
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return {'access_token': access_token,
                    'refresh_token': refresh_token,
                    'uid': user_db.id
                    }

    raise HTTPException(status_code=404, detail="User not found")



@router.patch("/update", response_model=SchemaUser.User, status_code=200)
def update_user(name: str=Form(...), 
                lastname: str=Form(...),
                email: str=Form(...),
                phone_number: str=Form(...),
                username: str=Form(...),
                password: str=Form(...),
                avatar: UploadFile = File(...),
                db:Session=Depends(get_db),
                user_auth_dict=Depends(user_auth_middleware)):
    
    
    user = db.query(ModelUser.User).filter(ModelUser.User.id == user_auth_dict["uid"]).first()
    if user:
        hashed_pw = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
        user.name = name
        user.lastname = lastname
        user.email = email
        user.phone_number = phone_number
        user.username = username
        user.password = hashed_pw
        avatar_obj = BucketObj(file=avatar.file,
                           save_name=str(user.name),
                           destination="/sharksport/profiles",
                           format_="jpg")
        avatar_obj.upload_image()
        user.avatar_link = avatar_obj.perma_link()
        user.modified_at = current_time()

        db.commit()
        return user
    raise HTTPException(status_code=404, detail="User not found")




@admin_router.get("/list_users", status_code=200)
def list_users(db: Session=Depends(get_db), limit: int=10, admin_auth=Depends(admin_auth_middleware)):
    users = db.query(ModelUser.User).limit(limit).all()
    return users


@admin_router.delete("/delete_user")
def delete_user(user_id: str, db: Session=Depends(get_db), admin_auth=Depends(admin_auth_middleware)):
    user = db.query(ModelUser.User).filter(ModelUser.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return user