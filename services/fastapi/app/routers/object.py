"""Object routers."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.db import get_session

router = APIRouter(prefix="/api/v1", tags=["Objects"])


@router.get("/objects/{object_id}", response_model=schemas.ObjectResponseSingle)
def get_object(object_id: int, db: Annotated[Session, Depends(get_session)]) -> dict:
    """Get object.

    :param object_id: _description_
    :type object_id: int
    :param db: _description_
    :type db: Annotated[Session, Depends
    :raises HTTPException: _description_
    :raises HTTPException: _description_
    :return: _description_
    :rtype: _type_
    """
    comments_count = db.execute(
        select(func.count(models.Comment.id)).where(
            models.Comment.object_id == object_id
        )
    ).scalar()
    stmt = (
        select(
            models.Object,
            models.User,
            models.City,
            models.Category,
            models.Transaction,
        )
        .join(models.User, models.Object.user_id == models.User.id)
        .join(models.City, models.Object.city_id == models.City.id)
        .join(models.Category, models.Object.category_id == models.Category.id)
        .join(models.Transaction, models.Object.transaction_id == models.Transaction.id)
        .where(models.Object.id == object_id)
    )
    try:
        row = db.execute(stmt).one()
    except NoResultFound:
        raise HTTPException(404, "Object not found") from None
    except MultipleResultsFound:
        raise HTTPException(400, "Multiple objects found") from None

    obj, user, city, category, transaction = row
    return {
        "object": obj,
        "user": user,
        "city": city,
        "category": category,
        "transaction": transaction,
        "comments_count": comments_count or 0,
    }


@router.get("/objects/", response_model=schemas.PaginatedObject)
async def get_objects(
    db: Annotated[Session, Depends(get_session)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 3,
    category_id: Annotated[
        int | None, Query(description="ID категории (необязательный)")
    ] = None,
) -> dict:
    """_summary_.

    :param db: _description_
    :type db: Annotated[Session, Depends
    :param page: _description_, defaults to 1)]=1
    :type page: Annotated[int, Query, optional
    :param limit: _description_, defaults to 1, le=100)]=3
    :type limit: Annotated[int, Query, optional
    :param category_id: _description_, defaults to "ID категории (необязательный)") ]=None
    :type category_id: Annotated[ int  |  None, Query, optional
    :return: _description_
    :rtype: dict
    """
    offset = (page - 1) * limit

    stmt = select(func.count(models.Object.id))
    if category_id is not None:
        stmt = stmt.where(models.Object.category_id == category_id)
    total = db.scalar(stmt)

    category_name = None
    if category_id is not None:
        name_stmt = select(models.Category.title).where(
            models.Category.id == category_id
        )
        category_name = db.scalar(name_stmt)

    subq = (
        select(models.Comment.object_id, func.count(models.Comment.id).label("cnt"))
        .group_by(models.Comment.object_id)
        .subquery()
    )
    stmt = (
        select(
            models.Object,
            models.User,
            models.City,
            models.Category,
            models.Transaction,
            func.coalesce(subq.c.cnt, 0).label("comments_count"),
        )
        .join(models.User, models.Object.user_id == models.User.id)
        .join(models.City, models.Object.city_id == models.City.id)
        .join(models.Category, models.Object.category_id == models.Category.id)
        .join(models.Transaction, models.Object.transaction_id == models.Transaction.id)
        .outerjoin(subq, models.Object.id == subq.c.object_id)
        .order_by(models.Object.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    # Добавляем WHERE только если category_id передан
    if category_id is not None:
        stmt = stmt.where(models.Object.category_id == category_id)

    rows = db.execute(stmt).all()

    results = [
        {
            "object": obj,
            "user": user,
            "city": city,
            "category": category,
            "transaction": transaction,
            "comments_count": cnt,
        }
        for obj, user, city, category, transaction, cnt in rows
    ]

    return {
        "count": total,
        "results": results,
        "category_name": category_name,
        "category_id": category_id,
    }
