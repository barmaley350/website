from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.dependencies import get_session
from app.schemas import StatResponse

router = APIRouter(prefix="/api/v1", tags=["Stats"])


@router.get("/stats/", response_model=StatResponse)
async def get_stats(
    db: Annotated[AsyncSession, Depends(get_session)],
):
    stmt = (
        select(
            models.City.title,  # или models.City.id, если нужно
            func.count(models.Object.id).label("object_count"),
        )
        .join(models.Object, models.City.id == models.Object.city_id)  # INNER JOIN
        .group_by(models.City.id)  # группируем по городу
        .order_by(desc("object_count"))
        .limit(5)
    )

    result = await db.execute(stmt)
    cities = result.all()

    cities_stats = [{"city": city.title, "count": city.object_count} for city in cities]

    #
    stmt = (
        select(
            models.Category.title,  # или models.City.id, если нужно
            func.count(models.Object.id).label("object_count"),
        )
        .join(
            models.Category, models.Object.category_id == models.Category.id
        )  # INNER JOIN
        .group_by(models.Category.id)  # группируем по городу
        .order_by(desc("object_count"))
        .limit(5)
    )

    result = await db.execute(stmt)
    categories = result.all()
    categories_stats = [
        {"category": category.title, "count": category.object_count}
        for category in categories
    ]

    #
    stmt = (
        select(
            models.Transaction.title,  # или models.City.id, если нужно
            func.count(models.Object.id).label("object_count"),
        )
        .join(
            models.Transaction, models.Object.transaction_id == models.Transaction.id
        )  # INNER JOIN
        .group_by(models.Transaction.id)  # группируем по городу
        .order_by(desc("object_count"))
        .limit(5)
    )

    result = await db.execute(stmt)
    transactions = result.all()
    transactions_stats = [
        {"transaction": transaction.title, "count": transaction.object_count}
        for transaction in transactions
    ]

    return {
        "cities": cities_stats,
        "categories": categories_stats,
        "transactions": transactions_stats,
    }
