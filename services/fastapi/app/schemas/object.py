from datetime import datetime

from pydantic import BaseModel

from app.schemas import (
    category,
    city,
    transaction,
    user,
)


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
    category_id: int
    city_id: int
    transaction_id: int
    user_id: int
    created_at: datetime


class ObjectResponseWithRelations(BaseModel):
    object: ObjectResponse
    user: user.UserResponse
    city: city.CityResponse
    category: category.CategoryResponse
    transaction: transaction.TransactionResponse
    comments_count: int | None = None
    # similar_objects: list[ObjectResponse] | None = None

    class Config:
        from_attributes = True  # раньше orm_mode


class PaginatedObjectsResponse(BaseModel):
    count: int | None = None
    category_id: int | None = None
    category_name: str | None = None
    results: list[ObjectResponseWithRelations]


class RelatedObjectsResponse(BaseModel):
    results: list[ObjectResponseWithRelations]
