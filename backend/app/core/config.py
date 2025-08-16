import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "people-counter-api"
    API_PREFIX: str = "/api"

    POSTGRES_USER: str = Field("admin", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("people_counter", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("db", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field("5432", env="POSTGRES_PORT")

    BACKEND_HOST: str = Field("0.0.0.0", env="BACKEND_HOST")
    BACKEND_PORT: int = Field(8008, env="BACKEND_PORT")

    FRONTEND_ORIGIN: str = Field("http://localhost:3000", env="FRONTEND_ORIGIN")

    # STATIC_DIR: str = Field("app/app/static", env="STATIC_DIR")
    STORAGE_DIR: str = Field("app/app/static/", env="STORAGE_DIR")
    BASE_URL: str = Field("http://localhost:8008", env="BASE_URL")

    @property
    def DATABASE_URL(self) -> str:
        return (f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    class Config:
        env_file = ".env"

settings = Settings()