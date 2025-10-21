from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ----- Entrées -----
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OAuthUserCreate(BaseModel):
    email: EmailStr
    username: str
    provider: str
    provider_id: str
    avatar_url: Optional[str] = None

# ----- Sorties -----
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    provider: str
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True