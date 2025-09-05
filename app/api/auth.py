from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
# Ajoutez cet import
from app.core.security import verify_password, get_password_hash, create_access_token
from app.dependencies import get_db, get_user_service
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService
from app.core.security import create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.create_user(user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(
    login_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.authenticate_user(login_data.email, login_data.password)