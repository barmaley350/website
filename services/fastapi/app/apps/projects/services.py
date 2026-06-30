# app/services/object_service.py
from typing import Any

from app.apps import models
from app.apps.projects.repositories import ProjectRepository


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def get_projects_related(self, obj: models.Project) -> dict[str, Any]:
        rows = await self.repo.get_similar_projects(obj=obj)
        renamed_rows = [
            {
                "project": r["Project"],
                "user": r["User"],
                "geo": r["Geo"],
                "category": r["Category"],
                "comments_count": r["comments_count"],
            }
            for r in rows
        ]

        return {
            "results": renamed_rows,
        }

    async def get_project(self, project_slug: str) -> dict[str, Any]:
        """Собирает все данные для ответа на запрос GET /projects/{project_slug}.

        Возвращает словарь, который можно сразу отдать как JSON.
        """
        # # Количество комментариев

        obj = await self.repo.get_project_by_slug(project_slug)
        return await self.repo.get_project(obj=obj)

    async def get_projects(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        """Формирует ответ для GET /projects/.

        Формирует ответ для GET /projects/:
        - общее количество (count)
        - список объектов с данными и числом комментариев
        - имя и ID категории (если фильтр задан)
        """
        offset = (page - 1) * limit

        # Получаем общее количество (для пагинации)
        total = await self.repo.get_projects_count(filters)

        # Если задан category_id, получаем его название
        category_name = await self.repo.get_category_name_by_id(filters)

        # Получаем сами объекты
        rows = await self.repo.get_projects(
            filters=filters,
            offset=offset,
            limit=limit,
        )

        return {
            "count": total,
            "results": rows,
            "category_name": category_name,
            "category_id": filters.get("category_id") if filters else None,
        }

    async def get_project_by_id(self, project_slug: str) -> models.Project | None:
        """Получает объект по его Slug или None, если не найден."""
        return await self.repo.get_project_by_slug(project_slug)
