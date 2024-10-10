from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from models import user as ModelUser
from schemas import user as SchemaUser
from db import get_db, Session
from datetime import timedelta
import jwt, bcrypt
from .admin import current_time
from tools import BucketObj
from middleware.auth_middleware import create_access_token, decode_token

REFRESH_TOKEN_EXPIRY = 2

router = APIRouter()



@router.post("/user/signup/", response_model=SchemaUser.CreateResp, status_code=201)
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



@router.post("/user/login/",response_model=SchemaUser.LoginResp ,status_code=200)
def login(credentials: SchemaUser.Login, db: Session=Depends(get_db)):
    user_db = db.query(ModelUser.User).filter(ModelUser.User.username == credentials.username).first()

    if user_db:
        check_hash_pw = bcrypt.checkpw(credentials.password.encode(), user_db.password)

        if check_hash_pw:
            access_token = create_access_token(
            user_data={
                'username': user_db.username,
                'uid': str(user_db.id)
            })
            refresh_token = create_access_token(
                user_data= {
                    'username': user_db.username,
                    'uid': str(user_db.id)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return {'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'username': user_db.username,
                        'uid': str(user_db.id)
                    }}

    raise HTTPException(status_code=404, detail="User not found")