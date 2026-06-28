from pydantic import BaseModel


class GeoResponse(BaseModel):
    id: int
    name: str
