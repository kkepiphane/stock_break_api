#app/startup.py
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.stock_movement_service import StockMovementService
from app.services.alert_service import AlertService

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