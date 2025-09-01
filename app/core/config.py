from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    app_env: str
    app_debug: bool
    app_port: int

    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    redis_host: str
    redis_port: int

    secret_key: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
