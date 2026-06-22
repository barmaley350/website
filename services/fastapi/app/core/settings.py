from sqlalchemy.orm import declarative_base

from app.core.core_settings.base_settings import MyBaseSettings
from app.core.core_settings.db_settings import DBSettings


class Settings(MyBaseSettings):
    db_settings: DBSettings = DBSettings() # type: ignore


settings = Settings()
Base = declarative_base()
