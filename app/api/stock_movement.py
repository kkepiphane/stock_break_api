from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import StockMovementCreate, StockMovementOut

router = APIRouter()

# CREATE stock movement
@router.post("/", response_model=StockMovementOut)
async def create_stock_movement(data: StockMovementCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == data.product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # mettre à jour la quantité
    product.quantity += data.change

    movement = StockMovement(**data.dict())
    db.add(movement)
    await db.commit()
    await db.refresh(movement)
    return movement

# READ movements of a product
@router.get("/product/{product_id}", response_model=list[StockMovementOut])
async def get_movements(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StockMovement).where(StockMovement.product_id == product_id))
    return result.scalars().all()
