from fastapi import HTTPException
from datetime import datetime
from models.user import User as UserModel
from models import user as UserModel
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










def update_address(address, db, uid):
    id = str(uuid.uuid4)
    new_address = UserModel.Address(id=id,
                               id_user=uid,
                               province=address.province,
                               city=address.city,
                               postal_code=address.postal_code,
                               detail=address.detail)

    db.add(new_address)
    db.commit()
    return new_address