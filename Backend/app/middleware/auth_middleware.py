from fastapi import HTTPException, Header
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os
import uuid
import logging
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
         
    