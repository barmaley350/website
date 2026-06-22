from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
ENV_PATH: Path | None = BASE_DIR / ".env"
ENV_FILE: str | None = str(ENV_PATH) if ENV_PATH and ENV_PATH.exists() else None


class MyBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="POSTGRES_",
        env_file_encoding="utf8",
        extra="ignore",
    )
