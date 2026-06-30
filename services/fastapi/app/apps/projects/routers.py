"""Object routers."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.apps.projects import schemas, services
from app.core.dependencies import get_project_service

router = APIRouter(prefix="/api/v1", tags=["Projects"])


@router.get(
    "/projects/{project_slug}/related/",
    response_model=schemas.RelatedProjectsResponse,
)
async def get_project_related(
    project_slug: str,
    service: Annotated[services.ProjectService, Depends(get_project_service)],
) -> dict:
    """Получить связанные projects."""
    obj = await service.get_project_by_id(project_slug)
    return await service.get_projects_related(obj)


@router.get(
    "/projects/{project_slug}", response_model=schemas.ProjectResponseWithRelations
)
async def get_project(
    project_slug: str,
    service: Annotated[services.ProjectService, Depends(get_project_service)],
) -> dict:
    """Получить project по его ID.

    Возвращает полную информацию об project, включая связанные данные:
    пользователя, город, категорию, транзакцию и количество комментариев.
    """  # noqa: RUF002 TODO: fix later
    return await service.get_project(project_slug)


@router.get("/projects/", response_model=schemas.PaginatedProjectsResponse)
async def get_projects(
    service: Annotated[services.ProjectService, Depends(get_project_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 3,
    category_id: Annotated[
        int | None, Query(description="ID категории (необязательный)")
    ] = None,
) -> dict:
    """Получить список project с пагинацией и фильтрацией по категории.

    Возвращает project, отсортированные по дате создания (новые сверху).
    Каждый project содержит связанные данные: пользователя, город, категорию,
    транзакцию и количество комментариев.
    """  # noqa: RUF002 TODO: fix later
    filters = {
        "category_id": category_id,
    }
    return await service.get_projects(
        page=page,
        limit=limit,
        filters=filters,
    )
