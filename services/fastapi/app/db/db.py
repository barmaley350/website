import os
from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

path_to_env_local = Path.cwd().parent.parent / ".env"

if path_to_env_local.exists():
    env_vars = dotenv_values(path_to_env_local)
    POSTGRES_HOST = "localhost"
    POSTGRES_DB = env_vars.get("POSTGRES_DB")
    POSTGRES_USER = env_vars.get("POSTGRES_USER")
    POSTGRES_PASSWORD = env_vars.get("POSTGRES_PASSWORD")
    POSTGRES_PORT = env_vars.get("POSTGRES_PORT")
else:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
