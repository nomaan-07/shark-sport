from fastapi import APIRouter, HTTPException, status, Depends, File, Form, UploadFile
from db import Session, get_db
from schemas import admin as SchemaAdmin
from models import admin as ModelAdmin
from datetime import datetime
from middleware.auth_middleware import create_admin_access_token ,create_access_token, decode_token, admin_auth_middleware
import jwt, bcrypt
from tools import current_time, BucketObj


router = APIRouter(
     prefix="/admin"
)


@router.get("/get/current_admin")
def current_admin(db: Session=Depends(get_db), admin_auth=Depends(admin_auth_middleware)):
    current_admin = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.id == admin_auth["aid"]).first()
    if current_admin:
        return current_admin
    raise HTTPException(status_code=404, detail="Not found")

@router.get("/get/{admin_id}", response_model=SchemaAdmin.Admin, status_code=200)
def get_admin_by_id(admin_id: str, db: Session = Depends(get_db), admin_auth=Depends(admin_auth_middleware)):
    admin_db = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.id == admin_id).first()
    
    if admin_db:
        if admin_auth["root_access"]== True:
            return admin_db
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access denied")    
    raise HTTPException(status_code=404, detail="Admin not found")


# craete admin
@router.post('/create', response_model=SchemaAdmin.createAdmin_resp, status_code=201) # admin depen inj is removed
def create_admin(name: str =Form(...),
                 lastname: str=Form(...),
                 username: str=Form(...),
                 email: str=Form(...),
                 phone: str=Form(...),
                 google_analytics_token: str=Form(default=None),
                 google_analyze_website: bool=Form(default=False),
                 instagram_token: str=Form(default=None),
                 root_access: bool=Form(...),
                 password: str=Form(...),
                 avatar: UploadFile =File(...),
                 db: Session=Depends(get_db)
                 ):#,admin_auth_dict=Depends(admin_auth_middleware)):
    admin_email = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.email == email).first()
    admin_username = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.username == username).first()
    if not admin_email and not admin_username:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        avatar_obj = BucketObj(avatar.file, username, "/sharksport/profiles", format_="jpg")
        avatar_obj.upload_image()
        avatar_link = avatar_obj.perma_link()

        new_admin = ModelAdmin.Admin(id= f'{name}-{username}-{phone[-3:]}',
                                    name=name,
                                    lastname=lastname,
                                    username=username,
                                    email=email,
                                    phone=phone,
                                    password = hashed_pw,
                                    avatar_link = avatar_link,
                                    google_analytics_token=google_analytics_token,
                                    google_analyze_website=google_analyze_website,
                                    instagram_token=instagram_token,
                                    root_access=root_access,
                                    created_at=current_time()
                                    )

        db.add(new_admin)
        db.commit()
        return new_admin
    raise HTTPException(status_code=404, detail="Duplicated username or email")



@router.patch('/update/{admin_id}', response_model=SchemaAdmin.SchemaAdminUpdate, status_code=200)
def update_admin(
    admin_id: str,
    name: str | None = Form(None),
    lastname: str | None = Form(None),
    username: str | None = Form(None),
    email: str | None = Form(None),
    phone: str | None = Form(None),
    google_analytics_token: str | None = Form(None),
    google_analyze_website: bool | None = Form(None),
    instagram_token: str | None = Form(None),
    root_access: bool | None = Form(None),
    password: str | None = Form(None),
    avatar: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    existing_admin = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.id == admin_id).first()
    
    if not existing_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if name is not None:
        existing_admin.name = name
    if lastname is not None:
        existing_admin.lastname = lastname
    if username is not None:
        existing_admin.username = username
    if email is not None:
        existing_admin.email = email
    if phone is not None:
        existing_admin.phone = phone
    if google_analytics_token is not None:
        existing_admin.google_analytics_token = google_analytics_token
    if google_analyze_website is not None:
        existing_admin.google_analyze_website = google_analyze_website
    if instagram_token is not None:
        existing_admin.instagram_token = instagram_token
    if root_access is not None:
        existing_admin.root_access = root_access
    if password is not None:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        existing_admin.password = hashed_pw
    if avatar is not None:
        avatar_obj = BucketObj(avatar.file, existing_admin.username, "/sharksport/profiles", format_="jpg")
        avatar_obj.upload_image()
        existing_admin.avatar_link = avatar_obj.perma_link()

    # Commit the changes to the database
    db.commit()
    
    return existing_admin


@router.post('/login',
            response_model=SchemaAdmin.LoginResp, 
            status_code=200)
def admin_login(credentials: SchemaAdmin.Login, db: Session=Depends(get_db)):
    admin = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.username == credentials.username).first()
    if admin:
        access_token = create_admin_access_token(
            admin_data={
                'aid': admin.id,
                'root_access': admin.root_access
            })
        return {"access_token": access_token}
    raise HTTPException(status_code=404, detail="User not found")


@router.get('/get/', response_model=SchemaAdmin.Admin, status_code=200)
def get_admin_by_id(id: str, db: Session=Depends(get_db)):
    admin_db = db.query(ModelAdmin.Admin).filter(ModelAdmin.Admin.id == id).first()
    if admin_db:
            return admin_db
    raise HTTPException(status_code=404, detail="admin not found")

@router.post('/update_permission', response_model=SchemaAdmin.create_permission_resp,
        status_code=201
        )
def create_permission(permission_info: SchemaAdmin.BasePermission, db: Session=Depends(get_db)):
    data_dump = permission_info.model_dump()
    new_permission = ModelAdmin.Permission(**data_dump)

    db.add(new_permission)
    db.commit()
    return new_permission

