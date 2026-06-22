import os
from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

path_to_env_local = Path.cwd().parent.parent / ".env"

if path_to_env_local.exists():
    env_vars = dotenv_values(path_to_env_local)
    POSTGRES_DB_HOST = "localhost"
    POSTGRES_DB_NAME = env_vars.get("POSTGRES_DB_NAME")
    POSTGRES_DB_USER = env_vars.get("POSTGRES_DB_USER")
    POSTGRES_DB_PASSWORD = env_vars.get("POSTGRES_DB_PASSWORD")
    POSTGRES_DB_PORT = env_vars.get("POSTGRES_DB_PORT")
else:
    POSTGRES_DB_HOST = os.getenv("POSTGRES_DB_HOST")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
    POSTGRES_DB_USER = os.getenv("POSTGRES_DB_USER")
    POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_DB_PASSWORD")
    POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT")

Base = declarative_base()

ASYNC_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_DB_USER}:{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}"

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # важно для async!
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()
