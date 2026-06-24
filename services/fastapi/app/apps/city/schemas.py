from pydantic import BaseModel


class CityResponse(BaseModel):
    title: str
    description: str
