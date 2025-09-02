from pydantic import BaseModel
from datetime import datetime

# ----- Entrées -----
class StockMovementCreate(BaseModel):
    product_id: int
    change: int
    reason: str | None = None

# ----- Sorties -----
class StockMovementOut(BaseModel):
    id: int
    product_id: int
    change: int
    reason: str | None
    created_at: datetime

    class Config:
        orm_mode = True
