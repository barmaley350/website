from datetime import datetime

from pydantic import BaseModel


class StatResponse(BaseModel):
    cities: list
    categories: list
    transactions: list

    class Config:
        from_attributes = True  # раньше orm_mode
