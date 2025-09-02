from fastapi import APIRouter, Depends
from app.schemas.stock import StockUpdate
from app.services.stock_service import StockService

router = APIRouter()

@router.post("/update")
async def update_stock(data: StockUpdate, service: StockService = Depends()):
    return await service.update_stock(data.product_id, data.new_quantity)
