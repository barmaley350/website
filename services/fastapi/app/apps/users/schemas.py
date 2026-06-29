from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: str
    avatar_github: str | None
