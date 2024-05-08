from pydantic import Field
from pydantic import model_validator
from pydantic_settings import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    # APP SETTINGS
    APP_PREFIX: str
    APP_HOST: str
    APP_PORT: int
    APP_BASE_URL: str
    APP_LOG_LEVEL: str
    APP_SECRET_KEY: str
    APP_ALGORITHM: str
    APP_ACCESS_EXPIRE_DAYS: int = Field(default=30)
    APP_BROKER_URL: str
    APP_CACHE_URL: str
    APP_SUBJECT: str = Field(default="Academy Cloud")
    APP_SUPERUSER_ROLE_ID: int = Field(default=2)
    APP_MANAGER_ROLE_ID: int = Field(default=3)

    # SMTP Server
    SMTP_SERVER: str = Field(default="smtp.example.com")
    SMTP_PORT: int = Field(default=465)
    SMTP_LOGIN: str = Field(default="example@example.com")
    SMTP_PASSWORD: str = Field(default="example")
    SMTP_TOKEN_EXPIRE_DAYS: float = Field(default=0.5)

    # DB SETTINGS
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_URL: str = None

    @model_validator(mode="before")
    @classmethod
    def get_database_url(cls, v):
        v["DB_URL"] = "postgresql+asyncpg://" + \
            f"{v["DB_USER"]}:{v["DB_PASS"]}@" + \
            f"{v["DB_HOST"]}:{v["DB_PORT"]}/{v["DB_NAME"]}"
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
