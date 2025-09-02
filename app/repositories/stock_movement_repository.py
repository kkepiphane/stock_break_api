from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.stock_movement import StockMovement
from app.repositories.base import BaseRepository

class StockMovementRepository(BaseRepository[StockMovement]):
    def __init__(self, db: Session):
        super().__init__(StockMovement, db)

    def get_movements_by_product(self, product_id: int, skip: int = 0, limit: int = 100):
        return (
            self.db.query(StockMovement)
            .filter(StockMovement.product_id == product_id)
            .order_by(desc(StockMovement.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_recent_movements(self, days: int = 7, skip: int = 0, limit: int = 100):
        from sqlalchemy import func, text
        return (
            self.db.query(StockMovement)
            .filter(StockMovement.created_at >= func.date_sub(func.now(), text(f"INTERVAL {days} DAY")))
            .order_by(desc(StockMovement.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )