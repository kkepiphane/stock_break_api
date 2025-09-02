from pydantic import BaseModel

class StockUpdate(BaseModel):
    product_id: int
    new_quantity: int
