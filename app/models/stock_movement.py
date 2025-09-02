from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    change = Column(Integer, nullable=False)  # ex: -5 pour sortie, +10 pour entrée
    reason = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    product = relationship("Product", back_populates="movements")
