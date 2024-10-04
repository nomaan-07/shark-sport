from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from datetime import datetime
from schemas import user as UserSchema
from models.user import User as UserModel
from models import user as UserModel
from schemas import address as SchemaAddress
from db import get_db, Session
from crud import crud
from middleware.auth_middleware import auth_middleware
import bcrypt, uuid, jwt
from urllib.parse import quote
import os,boto3
from dotenv import load_dotenv
import os
load_dotenv()
PASSWORD_KEY = os.getenv("PASSWORD_KEY")

router = APIRouter()

LIARA_ENDPOINT = os.getenv("LIARA_ENDPOINT")
LIARA_ACCESS_KEY = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY = os.getenv("LIARA_SECRET_KEY")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    endpoint_url=LIARA_ENDPOINT,
    aws_access_key_id=LIARA_ACCESS_KEY,
    aws_secret_access_key=LIARA_SECRET_KEY,
)

router = APIRouter()




@router.post("/user/signup", response_model=UserSchema.User, status_code=201)
def signup(user: UserSchema.BaseUser, db: Session = Depends(get_db)):
    hash_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_id = str(uuid.uuid4())
    new_user = UserModel.User(id=str(user_id),
                         name=user.name,
                         last_name=user.last_name,
                         username=user.username,
                         password=hash_pw,
                         created_at = datetime.now().replace(second=0, microsecond=0))
    
    db.add(new_user)
    db.commit()
    return new_user




@router.post("/user/login", response_model=UserSchema.LoginResponse)
def login(user: UserSchema.UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(UserModel.User).filter(UserModel.User.username == user.username).first()

    if user_db == None :
        raise HTTPException(status_code=404, detail=f"Login Failed, User With {user.username} and Password not found")
    check_hash_pw = bcrypt.checkpw(user.password.encode(), user_db.password)
    if not check_hash_pw:
        raise HTTPException(status_code=404, detail=f"Login Failed, User With {user.username} and Password not found")
    token = jwt.encode(payload={"id": user_db.id}, key=PASSWORD_KEY)

    return {"token": token, "user": user_db}





@router.patch("/user/profile", response_model=UserSchema.User, status_code=200)
def update_user_profile(user_id: str, patch_data:UserSchema.SecondUSer, new_pic: UploadFile=File(...), db: Session=Depends(get_db), auth_dict= Depends(auth_middleware)):
    if not db.query(UserModel).filter(UserModel.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found!")
    else:
        pic_id = str(uuid.uuid4())
        pic_upload_res = s3.upload_fileobj(new_pic.file, LIARA_BUCKET_NAME, f'sharksport/images/profiles{pic_id}.jpg')
        pic_filename_encoded = quote(f'sharksport/images/profiles{pic_id}.jpg')
        pic_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{pic_filename_encoded}"

        user_db = db.query(UserModel.User).filter(UserModel.User.id == id).first()

        user_db.picture_url = pic_permanent_url
        user_db.username = patch_data.username
        user_db.name = patch_data.name
        user_db.last_name = patch_data.last_name
        user_db.email = patch_data.email
        user_db.phone = patch_data.phone
        user_db.telephone = patch_data.telephone
        user_db.password = user_db.password
        user_db.modified_at = datetime.now().replace(second=0, microsecond=0)


        db.commit()
        return user_db



@router.get("/user/")
def get_user_profile(uid: str, db: Session=Depends(get_db)):
    user_db = db.query(UserModel).filter(UserModel.id == uid).first()

    return user_db




@router.patch("/user/address", response_model=SchemaAddress.Address)
def create_address(address: SchemaAddress.BaseAddress, db: Session = Depends(get_db), auth_dict= Depends(auth_middleware)):
    

    pic_id = str(uuid.uuid4())
    id = str(uuid.uuid4)
    new_address = UserModel.Address(id=id,
                               id_user=auth_dict["uid"],
                               province=address.province,
                               city=address.city,
                               postal_code=address.postal_code,
                               modified_at=datetime.now().replace(second=0, microsecond=0),
                               detail=address.detail)

    db.add(new_address)
    db.commit()
    return new_address