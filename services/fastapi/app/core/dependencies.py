from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import AsyncSessionLocal
from app.repositories.object_repository import ObjectRepository
from app.services.object_service import ObjectService


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# Зависимость, которая возвращает репозиторий
async def get_object_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ObjectRepository:
    return ObjectRepository(session)


# Зависимость, которая возвращает сервис
async def get_object_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ObjectService:
    return ObjectService(session)
