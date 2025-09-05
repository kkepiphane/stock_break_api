from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_stock_movement_service
from app.schemas.stock_movement import StockMovementCreate, StockMovementOut
from app.services.stock_movement_service import StockMovementService
from app.dependencies import get_current_user

router = APIRouter(prefix="/stock-movements", tags=["stock movements"])

@router.post("/", response_model=StockMovementOut, status_code=status.HTTP_201_CREATED)
async def create_stock_movement(
    movement_create: StockMovementCreate,
    movement_service: StockMovementService = Depends(get_stock_movement_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        movement = movement_service.create_movement(movement_create)
        return movement
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[StockMovementOut])
async def get_all_movements(
    skip: int = 0,
    limit: int = 100,
    movement_service: StockMovementService = Depends(get_stock_movement_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    movements = movement_service.movement_repo.get_all(skip, limit)
    return movements

@router.get("/recent/", response_model=List[StockMovementOut])
async def get_recent_movements(
    days: int = 7,
    skip: int = 0,
    limit: int = 100,
    movement_service: StockMovementService = Depends(get_stock_movement_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    movements = movement_service.get_recent_movements(days, skip, limit)
    return movements

@router.get("/product/{product_id}", response_model=List[StockMovementOut])
async def get_product_movements(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    movement_service: StockMovementService = Depends(get_stock_movement_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    movements = movement_service.get_product_movements(product_id, skip, limit)
    return movements

@router.get("/{movement_id}", response_model=StockMovementOut)
async def get_movement(
    movement_id: int,
    movement_service: StockMovementService = Depends(get_stock_movement_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    movement = movement_service.movement_repo.get_by_id(movement_id)
    if not movement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock movement not found"
        )
    return movement