from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import app.models as models
from app.db.db import get_session
from app.schemas import PostResponse

router = APIRouter(prefix="/api/v1", tags=["Posts"])


@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_session)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/posts", response_model=list[PostResponse])
def get_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts
