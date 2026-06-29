from pydantic import BaseModel


class StatResponse(BaseModel):
    geos: list
    categories: list

    class Config:
        from_attributes = True  # раньше orm_mode
