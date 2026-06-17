"""Object routers."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app import schemas, services
from app.core.dependencies import get_object_service

router = APIRouter(prefix="/api/v1", tags=["Objects"])


@router.get(
    "/objects/{object_id}/related/",
    response_model=schemas.RelatedObjectsResponse,
)
async def get_object_related(
    object_id: int,
    service: Annotated[services.ObjectService, Depends(get_object_service)],
) -> dict:
    """Получить связанные объекты."""
    obj = await service.get_object_by_id(object_id)
    return await service.get_objects_related(obj)


@router.get("/objects/{object_id}", response_model=schemas.ObjectResponseWithRelations)
async def get_object(
    object_id: int,
    service: Annotated[services.ObjectService, Depends(get_object_service)],
) -> dict:
    """Получить объект по его ID.

    Возвращает полную информацию об объекте, включая связанные данные:
    пользователя, город, категорию, транзакцию и количество комментариев.
    """  # noqa: RUF002 TODO: fix later
    return await service.get_object(object_id)


@router.get("/objects/", response_model=schemas.PaginatedObjectsResponse)
async def get_objects(
    service: Annotated[services.ObjectService, Depends(get_object_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 3,
    category_id: Annotated[
        int | None, Query(description="ID категории (необязательный)")
    ] = None,
) -> dict:
    """Получить список объектов с пагинацией и фильтрацией по категории.

    Возвращает объекты, отсортированные по дате создания (новые сверху).
    Каждый объект содержит связанные данные: пользователя, город, категорию,
    транзакцию и количество комментариев.
    """  # noqa: RUF002 TODO: fix later
    filters = {
        "category_id": category_id,
    }
    return await service.get_objects(
        page=page,
        limit=limit,
        filters=filters,
    )
