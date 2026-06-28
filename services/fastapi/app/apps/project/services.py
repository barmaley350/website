# app/services/object_service.py
from typing import Any

from app.apps import models
from app.apps.project.repositories import ProjectRepository


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

    async def get_project(self, project_id: int) -> dict[str, Any]:
        """Собирает все данные для ответа на запрос GET /projects/{project_id}.

        Возвращает словарь, который можно сразу отдать как JSON.
        """
        # # Количество комментариев

        obj = await self.repo.get_project_by_id(project_id)
        rows = await self.repo.get_project(obj=obj)

        # Похожие объекты
        # similar_objects = await self.get_similar_objects(obj)

        return {
            "project": rows["Project"],
            "user": rows["User"],
            "geo": rows["Geo"],
            "category": rows["Category"],
            "comments_count": rows["comments_count"],
        }

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
            "count": total,
            "results": renamed_rows,
            "category_name": category_name,
            "category_id": filters.get("category_id") if filters else None,
        }

    async def get_project_by_id(self, project_id: int) -> models.Project | None:
        """Получает объект по его ID или None, если не найден."""
        return await self.repo.get_project_by_id(project_id)
