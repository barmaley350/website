from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.object.repositories import ObjectRepository
from app.apps.object.services import ObjectService
from app.core.core_dependencies.db_dependency import DBDependency

db = DBDependency()


async def get_session():
    async with db.db_session() as session:
        yield session


# Зависимость, которая возвращает репозиторий
async def get_object_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ObjectRepository:
    return ObjectRepository(session)


# Зависимость, которая возвращает сервис
async def get_object_service(
    repo: Annotated[ObjectRepository, Depends(get_object_repository)],
) -> ObjectService:
    return ObjectService(repo)
