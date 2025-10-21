from typing import Optional, Dict, Any
import requests
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, OAuthUserCreate
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
        user_data["provider"] = "email"  # Définir le provider comme "email"
        
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

    # Méthodes OAuth
    async def authenticate_google(self, access_token: str) -> Optional[User]:
        """Authentifier via Google OAuth"""
        try:
            # Récupérer les infos utilisateur de Google
            user_info = await self._get_google_user_info(access_token)
            
            # Chercher l'utilisateur par provider_id
            user = self.repository.db.query(User).filter(
                User.provider == "google",
                User.provider_id == user_info["sub"]
            ).first()
            
            if user:
                return user
            
            # Vérifier si l'email existe déjà avec un autre provider
            existing_user = self.repository.get_by_email(user_info["email"])
            if existing_user:
                # Mettre à jour le provider si l'email existe déjà
                updated_user = self.repository.update(existing_user, {
                    "provider": "google",
                    "provider_id": user_info["sub"],
                    "avatar_url": user_info.get("picture"),
                    "is_verified": user_info.get("email_verified", False)
                })
                return updated_user
            
            # Si l'utilisateur n'existe pas, le créer
            username = self._generate_unique_username(user_info["email"].split("@")[0])
            
            user_data = {
                "email": user_info["email"],
                "username": username,
                "provider": "google",
                "provider_id": user_info["sub"],
                "avatar_url": user_info.get("picture"),
                "is_verified": user_info.get("email_verified", False),
                "password_hash": None  # Pas de mot de passe pour OAuth
            }
            
            return self.repository.create(user_data)
            
        except Exception as e:
            print(f"Google OAuth error: {e}")
            return None

    async def authenticate_facebook(self, access_token: str) -> Optional[User]:
        """Authentifier via Facebook OAuth"""
        try:
            # Récupérer les infos utilisateur de Facebook
            user_info = await self._get_facebook_user_info(access_token)
            
            # Chercher l'utilisateur par provider_id
            user = self.repository.db.query(User).filter(
                User.provider == "facebook",
                User.provider_id == user_info["id"]
            ).first()
            
            if user:
                return user
            
            # Vérifier si l'email existe déjà avec un autre provider
            existing_user = self.repository.get_by_email(user_info.get("email", f"{user_info['id']}@facebook.com"))
            if existing_user:
                # Mettre à jour le provider si l'email existe déjà
                updated_user = self.repository.update(existing_user, {
                    "provider": "facebook",
                    "provider_id": user_info["id"],
                    "avatar_url": user_info.get("picture", {}).get("data", {}).get("url"),
                    "is_verified": True
                })
                return updated_user
            
            # Si l'utilisateur n'existe pas, le créer
            username = self._generate_unique_username(user_info.get("name", user_info["id"]).replace(" ", "_").lower())
            email = user_info.get("email", f"{user_info['id']}@facebook.com")
            
            user_data = {
                "email": email,
                "username": username,
                "provider": "facebook",
                "provider_id": user_info["id"],
                "avatar_url": user_info.get("picture", {}).get("data", {}).get("url"),
                "is_verified": True,
                "password_hash": None  # Pas de mot de passe pour OAuth
            }
            
            return self.repository.create(user_data)
            
        except Exception as e:
            print(f"Facebook OAuth error: {e}")
            return None

    async def _get_google_user_info(self, access_token: str) -> Dict[str, Any]:
        """Récupérer les informations utilisateur de Google"""
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    async def _get_facebook_user_info(self, access_token: str) -> Dict[str, Any]:
        """Récupérer les informations utilisateur de Facebook"""
        response = requests.get(
            "https://graph.facebook.com/me",
            params={
                "fields": "id,name,email,picture",
                "access_token": access_token
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def _generate_unique_username(self, base_username: str) -> str:
        """Générer un nom d'utilisateur unique"""
        username = base_username
        counter = 1
        
        while self.repository.get_by_username(username):
            username = f"{base_username}_{counter}"
            counter += 1
            
        return username