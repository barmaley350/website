from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models
from app.core.dependencies import get_session
from app.schemas import PaginatedResponse, PostResponse

router = APIRouter(prefix="/api/v1", tags=["Posts"])


@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_session)]):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/posts", response_model=PaginatedResponse)
async def get_posts(
    page: int = Query(1, ge=1),  # noqa: FAST002
    limit: int = Query(10, ge=1, le=100),  # noqa: FAST002
    db: Session = Depends(get_session),
):
    offset = (page - 1) * limit
    total = db.scalar(select(func.count()).select_from(models.Post))

    subq = (
        select(models.Comment.post_id, func.count(models.Comment.id).label("cnt"))
        .group_by(models.Comment.post_id)
        .subquery()
    )
    stmt = (
        select(
            models.Post,
            models.User,
            func.coalesce(subq.c.cnt, 0).label("comments_count"),
        )
        .join(models.User, models.Post.user_id == models.User.id)
        .outerjoin(subq, models.Post.id == subq.c.post_id)
        .order_by(models.Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    rows = db.execute(stmt).all()

    results = [
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "user_id": u.id,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"),
            "username": u.username,
            "email": u.email,
            "comments_count": cnt,
        }
        for p, u, cnt in rows
    ]

    return {"count": total, "results": results}
