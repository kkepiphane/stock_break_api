from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_product_service
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services.product_service import ProductService
from app.dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_create: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        product = product_service.create_product(product_create)
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# @router.get("/", response_model=List[ProductOut])
# async def get_all_products(
#     skip: int = 0,
#     limit: int = 100,
#     product_service: ProductService = Depends(get_product_service),
#     current_user: dict = Depends(get_current_user)
# ):
#     if current_user["role"] == "admin":
#         products = product_service.product_repo.get_all(skip, limit)
#     else:
#         # Seulement les produits actifs pour les non-admins
#         products = product_service.product_repo.get_active_products(skip, limit)
#     return products

@router.get("/", response_model=List[ProductOut])
async def get_all_products(
    skip: int = 0,
    limit: int = 100,
    product_service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)  # Authentification REQUISE
):
    products = product_service.product_repo.get_all(skip, limit)
    return products

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    product = product_service.product_repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.get("/sku/{sku}", response_model=ProductOut)
async def get_product_by_sku(
    sku: str,
    product_service: ProductService = Depends(get_product_service)
):
    product = product_service.product_repo.get_by_sku(sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.get("/low-stock/", response_model=List[ProductOut])
async def get_low_stock_products(
    threshold: int = None,
    product_service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    products = product_service.get_low_stock_products(threshold)
    return products

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    product = product_service.update_product(product_id, product_update)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    success = product_service.product_repo.delete(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )