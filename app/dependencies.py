import os
from dotenv import load_dotenv
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.stock_movement_service import StockMovementService
from app.services.alert_service import AlertService
from app.core.security import decode_token  # ← Import manquant
from jose import JWTError, jwt  # ← Import manquant
from app.core.config import settings  # ← Import manquant

load_dotenv() 
# Ajoutez ceci après les imports
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)

def get_stock_movement_service(db: Session = Depends(get_db)) -> StockMovementService:
    return StockMovementService(db)

def get_alert_service(db: Session = Depends(get_db)) -> AlertService:
    return AlertService(db)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    
    return user