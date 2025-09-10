from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, func, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(150), nullable=False)          # Nom du client
    customer_email = Column(String(150), nullable=True)          # Email du client
    customer_phone = Column(String(50), nullable=True)           # Téléphone du client
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)  # Montant total
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relations
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
