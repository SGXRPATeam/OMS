import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "OMS Backend"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        )
        extra = "ignore"


settings = Settings()