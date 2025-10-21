from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String(50), default="user")  # admin, commercial, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    provider = Column(String(50), default="email")  # 'email', 'google', 'facebook'
    provider_id = Column(String(255), nullable=True, unique=True)
    avatar_url = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False)
