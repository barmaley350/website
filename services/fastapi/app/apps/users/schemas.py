from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str
    phone: str
    avatar_github: str | None
