from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter()

@router.post('/login', response_model=None, status_code=status.HTTP_201_CREATED)
def signup(signup_data: None):
    return