from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.projects.repositories import ProjectRepository
from app.apps.projects.services import ProjectService
from app.core.core_dependencies.db_dependency import DBDependency

db = DBDependency()


async def get_session():
    async with db.db_session() as session:
        yield session

async def get_engine():
    return db.db_engine

# Зависимость, которая возвращает репозиторий
async def get_project_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProjectRepository:
    return ProjectRepository(session)


# Зависимость, которая возвращает сервис
async def get_project_service(
    repo: Annotated[ProjectRepository, Depends(get_project_repository)],
) -> ProjectService:
    return ProjectService(repo)
