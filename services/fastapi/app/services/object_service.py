# app/services/object_service.py
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.repositories.object_repository import ObjectRepository


class ObjectService:
    def __init__(self, session: AsyncSession):
        self.repo = ObjectRepository(session)

    async def get_similar_objects(self, obj: models.Object) -> list[models.Object]:
        return await self.repo.get_similar_objects(
            object_id=obj.id,
            city_id=obj.city_id,
            category_id=obj.category_id,
            transaction_id=obj.transaction_id,
        )

    async def get_object_response(self, object_id: int) -> dict[str, Any]:
        """Собирает все данные для ответа на запрос GET /objects/{object_id}.

        Возвращает словарь, который можно сразу отдать как JSON.
        """
        # Получаем объект и связанные сущности
        (
            obj,
            user,
            city,
            category,
            transaction,
        ) = await self.repo.get_object_with_relations(object_id)

        # Количество комментариев
        comments_count = await self.repo.get_comments_count(object_id)

        # Похожие объекты
        similar_objects = await self.get_similar_objects(obj)

        return {
            "object": obj,
            "user": user,
            "city": city,
            "category": category,
            "transaction": transaction,
            "comments_count": comments_count,
            "similar_objects": similar_objects,
        }

    async def get_objects_response(
        self,
        page: int = 1,
        limit: int = 10,
        category_id: int | None = None,
    ) -> dict[str, Any]:
        """Формирует ответ для GET /objects/.

        Формирует ответ для GET /objects/:
        - общее количество (count)
        - список объектов с данными и числом комментариев
        - имя и ID категории (если фильтр задан)
        """
        offset = (page - 1) * limit

        # Получаем общее количество (для пагинации)
        total = await self.repo.get_objects_count(category_id)

        # Если задан category_id, получаем его название
        category_name = None
        if category_id is not None:
            category_name = await self.repo.get_category_name(category_id)

        # Получаем сами объекты
        rows = await self.repo.get_objects_with_comments(
            category_id=category_id,
            offset=offset,
            limit=limit,
        )

        # Преобразуем кортежи в удобный для ответа список
        results = [
            {
                "object": obj,
                "user": user,
                "city": city,
                "category": category,
                "transaction": transaction,
                "comments_count": cnt,
            }
            for obj, user, city, category, transaction, cnt in rows
        ]

        return {
            "count": total,
            "results": results,
            "category_name": category_name,
            "category_id": category_id,
        }
