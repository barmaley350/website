from pydantic import BaseModel


class CategoryResponse(BaseModel):
    title: str
    description: str
