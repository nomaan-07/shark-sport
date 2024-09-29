from fastapi import APIRouter, Depends
from schemas import user as UserSchema
from db import get_db, Session
from crud import crud



router = APIRouter()




@router.post("/auth/signup", response_model=UserSchema.User, status_code=201)
def signup(user: UserSchema.UserBase, db: Session = Depends(get_db)):
    return crud.create_user(user=user, db=db)


@router.post("/auth/login", response_model=UserSchema.LoginResponse)
def login(user: UserSchema.UserLogin, db: Session = Depends(get_db)):
    return crud.Login_user(user= user, db= db)