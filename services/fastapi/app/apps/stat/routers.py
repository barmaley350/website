from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps import models
from app.apps.stat.schemas import StatResponse
from app.core.dependencies import get_session

router = APIRouter(prefix="/api/v1", tags=["Stats"])


@router.get("/stats/", response_model=StatResponse)
async def get_stats(
    db: Annotated[AsyncSession, Depends(get_session)],
):
    stmt = (
        select(
            models.Geo.name,
            func.count(models.Project.id).label("project_count"),
        )
        .join(models.Project, models.Geo.id == models.Project.geo_id)  # INNER JOIN
        .group_by(models.Geo.id)  # группируем по городу
        .order_by(desc("project_count"))
        .limit(5)
    )

    result = await db.execute(stmt)
    geos = result.all()

    geos_stats = [{"geo": geo.name, "count": geo.project_count} for geo in geos]

    #
    stmt = (
        select(
            models.Category.name,  # или models.City.id, если нужно
            func.count(models.Project.id).label("project_count"),
        )
        .join(
            models.Category, models.Project.category_id == models.Category.id
        )  # INNER JOIN
        .group_by(models.Category.id)  # группируем по городу
        .order_by(desc("project_count"))
        .limit(5)
    )

    result = await db.execute(stmt)
    categories = result.all()
    categories_stats = [
        {"category": category.name, "count": category.project_count}
        for category in categories
    ]

    return {
        "geos": geos_stats,
        "categories": categories_stats,
    }
