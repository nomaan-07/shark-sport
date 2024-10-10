from fastapi import APIRouter, HTTPException, Depends
from db import Session, get_db
from schemas import admin as SchemaAdmin
from models import admin as ModelAdmin
from datetime import datetime
from middleware.auth_middleware import create_access_token, decode_token
import jwt, bcrypt

router = APIRouter()


def current_time() -> datetime: 
    time = datetime.now().replace(second=0, microsecond=0)
    
    return time

@router.post('/create_admin', response_model=SchemaAdmin.createAdmin_resp, status_code=201)
def create_admin(admin_dict: SchemaAdmin.BaseAdmin, db: Session=Depends(get_db)):

    hashed_pw = bcrypt.hashpw(admin_dict.password.encode(), bcrypt.gensalt())
    avatar_link = None

    new_admin = ModelAdmin.Admin(name=admin_dict.name,
                                 lastname=admin_dict.lastname,
                                 username=admin_dict.username,
                                 email=admin_dict.email,
                                 phone=admin_dict.phone,
                                 password = hashed_pw,
                                 avatar_link = avatar_link,
                                 google_analytics_token=admin_dict.google_analytics_token,
                                 google_analyze_website=admin_dict.google_analyze_website,
                                 instagram_token=admin_dict.instagram_token,
                                 root_access=admin_dict.root_access,
                                 created_at=current_time()
                                 )

    return new_admin

@router.post('/admin_login', response_model=SchemaAdmin.LoginResp, status_code=200)
def admin_login(credentials: SchemaAdmin.Login, db: Session=Depends(get_db)):
    admin = db.query(ModelAdmin.Admin).filter((ModelAdmin.Admin.email or ModelAdmin.Admin.phone) == credentials.username).first()
    return admin


@router.get('/get_admin/', response_model=SchemaAdmin.Admin, status_code=200)
def get_admin_by_id(id: int, db: Session=Depends(get_db)):
    admin_db = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.id == id).first()
    if admin_db:
            return admin_db
    raise HTTPException(status_code=404, detail="admin not found")

@router.post(
        '/create_admin/create_permission', response_model=SchemaAdmin.create_permission_resp,
        status_code=201
        )
def create_permission(permission_info: SchemaAdmin.BasePermission, db: Session=Depends(get_db)):
    data_dump = permission_info.model_dump()
    new_permission = ModelAdmin.Permission(**data_dump)

    db.add(new_permission)
    db.commit()
    return new_permission