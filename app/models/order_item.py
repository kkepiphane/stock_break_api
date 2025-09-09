from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, func, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False, default=0.00)

    # Relations
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
