from fastapi import HTTPException, Header
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os
import uuid
import logging
import bcrypt
import hashlib
load_dotenv()

PASSWORD_KEY = os.getenv("PASSWORD_KEY")
ALGORITH = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY = 3600

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool=False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + ( expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4)
    payload['refresh'] = refresh
    token = jwt.encode(
         payload=payload, key=PASSWORD_KEY, algorithm=ALGORITH
    )

    return token

def create_admin_access_token(admin_data: dict, expiry: timedelta = None, refresh: bool=False):
    payload = {}

    payload['admin'] = admin_data
    payload['exp'] = datetime.now() + ( expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4)
    payload['refresh'] = refresh
    token = jwt.encode(
         payload=payload, key=PASSWORD_KEY, algorithm=ALGORITH
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=PASSWORD_KEY,
            algorithms=ALGORITH
     )
        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None 
         
    

def check_pw(pw: str, hashed_pw: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode(), hashed_pw.encode())
    except Exception as e:
        raise RuntimeError("Password verification failed") from e

def hash_pw(pw: str) -> str:
    try:
        return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    except Exception as e:
        raise NotImplementedError("Algorithm not supported") from e





def user_auth_middleware(x_auth_token = Header()):
    try:
        if not x_auth_token:
            raise HTTPException(status_code=401, detail="No auth token, access denied")
        
        verified_token = jwt.decode(jwt=x_auth_token, key=PASSWORD_KEY, algorithms=ALGORITH)
        if verified_token:
            uid = verified_token.get("user").get("uid")
            return {"token": x_auth_token, "uid":uid}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token is not valid , auth proccess faile!")    





def admin_auth_middleware(x_auth_token = Header()):
    try:
        if not x_auth_token:
            raise HTTPException(status_code=401, detail="No auth token, access denied")
        
        verified_token = decode_token(x_auth_token)
        if verified_token:
            aid = verified_token.get("admin").get("aid")
            root_access = verified_token.get("admin").get("root_access")
            return {"token": x_auth_token, "aid":aid, "root_access":root_access}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token is not valid , auth proccess faile!")  