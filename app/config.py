from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    some_attr: str


class DBSettings(BaseSettings):
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


db_settings = DBSettings()
