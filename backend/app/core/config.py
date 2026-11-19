from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    APP_NAME: str = "CODE WIBES"
    APP_ENV: str = "development"

    PGHOST: str = "127.0.0.1"
    PGPORT: int = 5432
    PGDATABASE: str = "code_wibes"
    PGUSER: str = "code_wibes"
    PGPASSWORD: str
    GOOGLE_MAPS_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=BACKEND_ENV_FILE,
        extra="ignore",
    )


settings = Settings()
