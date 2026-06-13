from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import app.models as models
from app.db.db import get_session
from app.schemas import ObjectResponse, PaginatedObject

router = APIRouter(prefix="/api/v1", tags=["Objects"])


@router.get("/objects/{object_id}", response_model=ObjectResponse)
def get_object(post_id: int, db: Annotated[Session, Depends(get_session)]):
    post = db.query(models.Object).filter(models.Object.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Object not found")
    return post


@router.get("/objects", response_model=PaginatedObject)
async def get_objects(
    page: int = Query(1, ge=1),  # noqa: FAST002
    limit: int = Query(3, ge=1, le=100),  # noqa: FAST002
    db: Session = Depends(get_session),
):
    offset = (page - 1) * limit
    total = db.scalar(select(func.count()).select_from(models.Object))

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

    rows = db.execute(stmt).all()

    results = [
        {
            "id": o.id,
            "title": o.title,
            "description": o.description,
            "price": o.price,
            "is_active": o.is_active,
            "category": cat.title,
            "city": city.title,
            "transaction": tran.title,
            "user_id": u.id,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M"),
            "username": u.username,
            "email": u.email,
            "phone": u.phone,
            "comments_count": cnt,
        }
        for o, u, city, cat, tran, cnt in rows
    ]

    return {"count": total, "results": results}
