from fastapi import HTTPException, Header, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from typing import Annotated
from db import Session, get_db
from datetime import datetime, timedelta
from tools import current_time
import jwt
from dotenv import load_dotenv
import os
import uuid
import logging
import bcrypt
import hashlib
load_dotenv()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="api/admin")
PASSWORD_KEY = os.getenv("PASSWORD_KEY")
ALGORITH = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY = 3600


api_oauth_scheme = OAuth2PasswordBearer(tokenUrl="api")


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool=False):
    payload = {}
    payload['user'] = user_data
    payload['exp'] = current_time() + ( expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4)
    payload['refresh'] = refresh
    token = jwt.encode(
         payload=payload, key=PASSWORD_KEY, algorithm=ALGORITH
    )
    return token



def decode_token(token: str) -> dict:
    try:
        return jwt.decode(jwt=token, key=PASSWORD_KEY, algorithms=ALGORITH)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token is not valid , auth proccess faile!")  





def auth_middleware(x_auth_token = Depends(api_oauth_scheme)):
    try:
        if not x_auth_token:
            raise HTTPException(status_code=401, detail="No auth token, access denied")
        verified_token = jwt.decode(jwt=x_auth_token, key=PASSWORD_KEY, algorithms=ALGORITH)
        if verified_token:
            uid = verified_token.get("user").get("uid")
            user_type = verified_token["user"]["user_type"]
            refresh_mode = verified_token.get("refresh")
            message =  {"uid":uid, "user_type": user_type, "refresh":refresh_mode}
            if user_type == "admin":
                message["root_access"] =verified_token["user"]["root_access"]
            return message
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token is not valid , auth proccess faile!")      



def optional_auth_middleware(x_auth_token = Header(None)):
    if x_auth_token:
        try:
            verified_token = jwt.decode(jwt=x_auth_token, key=PASSWORD_KEY, algorithms=ALGORITH)
            uid = verified_token.get("user").get("uid")
            refresh_mode = verified_token.get("refresh")
            return {"uid": uid, "refresh": refresh_mode}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token is not valid, auth process failed!")



def get_current_user(x_auth_token=Depends(auth_middleware), db:Session=Depends(get_db)):
    return x_auth_token
        

def check_pw(pw: str, hashed_pw: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode(), hashed_pw)
    except Exception as e:
        raise RuntimeError("Password verification failed") from e

def hash_pw(pw: str) -> str:
    try:
        return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    except Exception as e:
        raise NotImplementedError("Algorithm not supported") from e