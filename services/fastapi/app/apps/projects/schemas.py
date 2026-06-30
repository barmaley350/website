from datetime import datetime

from pydantic import BaseModel

from app.apps.schemas import (
    CategoryResponse,
    GeoResponse,
    UserResponse,
)


class ProjectCreate(BaseModel):
    title: str
    content: str
    user_id: int


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    description_full: str | None
    is_active: bool
    category_id: int
    geo_id: int
    user_id: int
    created_at: datetime
    slug: str | None = None


class ProjectResponseWithRelations(BaseModel):
    project: ProjectResponse
    user: UserResponse
    geo: GeoResponse
    category: CategoryResponse
    comments_count: int | None = None
    user_skills: list[str] | None = None
    project_skills: list[str] | None = None
    team_users: list[UserResponse] | None = None

    class Config:
        from_attributes = True  # раньше orm_mode


class PaginatedProjectsResponse(BaseModel):
    count: int | None = None
    category_id: int | None = None
    category_name: str | None = None
    results: list[ProjectResponseWithRelations]


class RelatedProjectsResponse(BaseModel):
    results: list[ProjectResponseWithRelations]
