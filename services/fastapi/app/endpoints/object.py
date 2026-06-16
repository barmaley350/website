"""Object routers."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas, services
from app.core.dependencies import get_object_service, get_session

router = APIRouter(prefix="/api/v1", tags=["Objects"])


# @router.get(
#     "/objects/{object_id}/related/", response_model=list[schemas.ObjectResponseSingle]
# )
# async def get_object_related(
#     object_id: int,
#     service: Annotated[services.ObjectService, Depends(get_object_service)],
# ) -> dict:
#     """Получить связанные объекты."""

#     return await service.get_similar_objects()


@router.get("/objects/{object_id}", response_model=schemas.ObjectResponseSingle)
async def get_object(
    object_id: int,
    service: Annotated[services.ObjectService, Depends(get_object_service)],
) -> dict:
    """Получить объект по его ID.

    Возвращает полную информацию об объекте, включая связанные данные:
    пользователя, город, категорию, транзакцию и количество комментариев.
    """
    return await service.get_object_response(object_id)


@router.get("/objects/", response_model=schemas.PaginatedObject)
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
    """
    return await service.get_objects_response(
        page=page,
        limit=limit,
        category_id=category_id,
    )
