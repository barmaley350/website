from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: str
    username: str
    email: str
    comments_count: int

    class Config:
        from_attributes = True  # раньше orm_mode


class PaginatedResponse(BaseModel):
    count: int
    results: list[PostResponse]
