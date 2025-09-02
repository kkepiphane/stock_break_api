from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_create: UserCreate) -> User:
        # Vérifier si l'email existe déjà
        if self.repository.get_by_email(user_create.email):
            raise ValueError("Email already registered")
        
        # Vérifier si le username existe déjà
        if self.repository.get_by_username(user_create.username):
            raise ValueError("Username already taken")

        hashed_password = get_password_hash(user_create.password)
        user_data = user_create.dict(exclude={"password"})
        user_data["password_hash"] = hashed_password
        
        return self.repository.create(user_data)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_email(email)

    def update_user_role(self, user_id: int, role: str) -> Optional[User]:
        user = self.repository.get_by_id(user_id)
        if user:
            return self.repository.update(user, {"role": role})
        return None