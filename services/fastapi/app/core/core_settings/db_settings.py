from pathlib import Path

from pydantic import SecretStr

from app.core.core_settings.base_settings import MyBaseSettings


class DBSettings(MyBaseSettings):
    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: str
    db_echo: bool

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"  # type: ignore
