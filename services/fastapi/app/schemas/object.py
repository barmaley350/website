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


class ObjectResponse1(BaseModel):
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


class ObjectResponseSingle(BaseModel):
    object: ObjectResponse1
    user: user.UserResponse
    city: city.CityResponse
    category: category.CategoryResponse
    transaction: transaction.TransactionResponse

    class Config:
        from_attributes = True  # раньше orm_mode


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
