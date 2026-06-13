from datetime import datetime

from pydantic import BaseModel


class ObjectCreate(BaseModel):
    title: str
    content: str
    user_id: int


class ObjectResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    is_active: bool
    category: str
    city: str
    transaction: str
    user_id: int
    created_at: str
    username: str
    email: str
    phone: str
    comments_count: int

    class Config:
        from_attributes = True  # раньше orm_mode


class PaginatedObject(BaseModel):
    count: int
    results: list[ObjectResponse]
