from fastapi import HTTPException
from datetime import datetime
from models.user import UserDB as UserModel
import bcrypt, uuid, jwt

from dotenv import load_dotenv
import os
load_dotenv()
PASSWORD_KEY = os.getenv("PASSWORD_KEY")

def create_user(user, db):
    hash_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_id = str(uuid.uuid4())
    new_user = UserModel(id=str(user_id),
                         name=user.name,
                         last_name=user.last_name,
                         username=user.username,
                         password=hash_pw,
                         created_at = datetime.now().replace(second=0, microsecond=0))
    
    db.add(new_user)
    db.commit()
    return new_user


def Login_user(user, db):
    user_db = db.query(UserModel).filter(UserModel.username == user.username).first()

    
    if user_db == None :
        raise HTTPException(status_code=404, detail=f"Login Failed, User With {user.username} and Password not found")
        
    check_hash_pw = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not check_hash_pw:
        raise HTTPException(status_code=404, detail=f"Login Failed, User With {user.username} and Password not found")

    token = jwt.encode(payload={"id": user_db.id}, key=PASSWORD_KEY)

    return {"token": token, "user": user_db}