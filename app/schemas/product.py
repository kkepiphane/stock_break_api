from pydantic import BaseModel
from datetime import datetime

# ----- Entrées -----
class ProductCreate(BaseModel):
    name: str
    sku: str
    quantity: int = 0
    min_threshold: int = 10

class ProductUpdate(BaseModel):
    quantity: int | None = None
    min_threshold: int | None = None

# ----- Sorties -----
class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    quantity: int
    min_threshold: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
