# app/services/object_service.py
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.repositories.object_repository import ObjectRepository


class ObjectService:
    def __init__(self, session: AsyncSession):
        self.repo = ObjectRepository(session)

    async def get_objects_related(self, obj: models.Object) -> dict[str, Any]:
        rows = await self.repo.get_similar_objects(obj=obj)
        renamed_rows = [
            {
                "object": r["Object"],
                "user": r["User"],
                "city": r["City"],
                "category": r["Category"],
                "transaction": r["Transaction"],
                "comments_count": r["comments_count"],
            }
            for r in rows
        ]

        return {
            "results": renamed_rows,
        }

    async def get_object(self, object_id: int) -> dict[str, Any]:
        """Собирает все данные для ответа на запрос GET /objects/{object_id}.

        Возвращает словарь, который можно сразу отдать как JSON.
        """
        # # Количество комментариев

        obj = await self.repo.get_object_by_id(object_id)
        rows = await self.repo.get_object(obj=obj)

        # Похожие объекты
        # similar_objects = await self.get_similar_objects(obj)

        return {
            "object": rows["Object"],
            "user": rows["User"],
            "city": rows["City"],
            "category": rows["Category"],
            "transaction": rows["Transaction"],
            "comments_count": rows["comments_count"],
            # "similar_objects": None,
        }

    async def get_objects(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        """Формирует ответ для GET /objects/.

        Формирует ответ для GET /objects/:
        - общее количество (count)
        - список объектов с данными и числом комментариев
        - имя и ID категории (если фильтр задан)
        """
        offset = (page - 1) * limit

        # Получаем общее количество (для пагинации)
        total = await self.repo.get_objects_count(filters)

        # Если задан category_id, получаем его название
        category_name = await self.repo.get_category_name_by_id(filters)

        # Получаем сами объекты
        rows = await self.repo.get_objects(
            filters=filters,
            offset=offset,
            limit=limit,
        )

        renamed_rows = [
            {
                "object": r["Object"],
                "user": r["User"],
                "city": r["City"],
                "category": r["Category"],
                "transaction": r["Transaction"],
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

    async def get_object_by_id(self, object_id: int) -> models.Object | None:
        """Получает объект по его ID или None, если не найден."""
        return await self.repo.get_object_by_id(object_id)
