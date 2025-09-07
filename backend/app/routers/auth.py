from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from  ..db import get_db
from ..crud import create_user
from ..services import hash_password, verify_password, create_access_token, get_current_user
from ..crud import get_user_by_email
from .. import schemas
from ..services import create_reset_token, reset_password
from datetime import timedelta

from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register_user(email: str, password: str, db: Session = Depends(get_db)):
    user_exists = get_user_by_email(db, email)
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    user = create_user(db, email, hashed_password)

    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> schemas.Token:
    user = get_user_by_email(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return schemas.Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@router.post("/request_reset")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user:
        return {"msg": "If the email exists, a reset token will be sent"}
    
    token = create_reset_token(email)
    return {"reset_token": token}

@router.post("/reset_password")
async def reset_password_endpoint(token: str = Query(...), new_password: str = Query(...), db: Session = Depends(get_db)):
    return reset_password(db, token, new_password)