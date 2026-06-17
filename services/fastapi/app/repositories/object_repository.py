from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class ObjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def get_object_with_relations(
    #     self, object_id: int
    # ) -> tuple[
    #     models.Object, models.User, models.City, models.Category, models.Transaction
    # ]:
    #     """Возвращает объект и все связанные сущности.

    #     Если не найден или найдено несколько — выбрасывает исключения.
    #     """
    #     stmt = (
    #         select(
    #             models.Object,
    #             models.User,
    #             models.City,
    #             models.Category,
    #             models.Transaction,
    #         )
    #         .join(models.User, models.Object.user_id == models.User.id)
    #         .join(models.City, models.Object.city_id == models.City.id)
    #         .join(models.Category, models.Object.category_id == models.Category.id)
    #         .join(
    #             models.Transaction,
    #             models.Object.transaction_id == models.Transaction.id,
    #         )
    #         .where(models.Object.id == object_id)
    #     )

    #     result = await self.session.execute(stmt)
    #     obj, user, city, category, transaction = result.one()
    #     return (obj, user, city, category, transaction)

    async def get_comments_count(self, object_id: int) -> int:
        """Количество комментариев к объекту."""
        stmt = select(func.count(models.Comment.id)).where(
            models.Comment.object_id == object_id
        )
        return (await self.session.execute(stmt)).scalar() or 0

    async def get_similar_objects(
        self,
        obj: models.Object,
        limit: int = 3,
    ):
        """Похожие объекты (по городу, категории, транзакции, исключая текущий)."""
        comments_subq = (
            select(models.Comment.object_id, func.count(models.Comment.id).label("cnt"))
            .group_by(models.Comment.object_id)
            .subquery()
        )

        # Основной запрос с выбором всех нужных полей
        stmt = (
            select(
                models.Object,
                models.User,
                models.City,
                models.Category,
                models.Transaction,
                func.coalesce(comments_subq.c.cnt, 0).label("comments_count"),
            )
            .join(models.User, models.Object.user_id == models.User.id)
            .join(models.City, models.Object.city_id == models.City.id)
            .join(models.Category, models.Object.category_id == models.Category.id)
            .join(
                models.Transaction,
                models.Object.transaction_id == models.Transaction.id,
            )
            .outerjoin(comments_subq, models.Object.id == comments_subq.c.object_id)
            .where(
                models.Object.city_id == obj.city_id,
                models.Object.category_id == obj.category_id,
                models.Object.transaction_id == obj.transaction_id,
                models.Object.id != obj.id,  # исключаем текущий объект
            )
            .limit(limit)
            # при необходимости можно добавить сортировку, например, по дате или по рейтингу
            .order_by(models.Object.created_at.desc())
        )

        # stmt = self.make_filters(filters=filters, stmt=stmt)

        return list((await self.session.execute(stmt)).mappings().all())

    async def get_objects_count(self, filters: dict[str, str] | None = None) -> int:
        """Общее количество объектов (с фильтром по категории, если указан)."""
        stmt = select(func.count(models.Object.id))
        stmt = self.make_filters(filters=filters, stmt=stmt)

        return (await self.session.execute(stmt)).scalar() or 0

    async def get_category_name_by_id(
        self, filters: dict[str, str] | None = None
    ) -> str | None:
        """Название категории по ID."""
        category_id = None
        if filters:
            category_id = filters.get("category_id", None)
        if category_id is None:
            return None

        stmt = select(models.Category.title).where(models.Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_objects(
        self,
        *,
        filters: dict[str, str],
        offset: int = 0,
        limit: int = 10,
    ) -> list[RowMapping]:
        """Возвращает список объектов с пагинацией.

        Возвращает список объектов с пагинацией фильтром по категории,
        отсортированных по created_at DESC, с числом комментариев.
        """
        # Подзапрос для подсчёта комментариев
        comments_subq = (
            select(models.Comment.object_id, func.count(models.Comment.id).label("cnt"))
            .group_by(models.Comment.object_id)
            .subquery()
        )

        stmt = (
            select(
                models.Object,
                models.User,
                models.City,
                models.Category,
                models.Transaction,
                func.coalesce(comments_subq.c.cnt, 0).label("comments_count"),
            )
            .join(models.User, models.Object.user_id == models.User.id)
            .join(models.City, models.Object.city_id == models.City.id)
            .join(models.Category, models.Object.category_id == models.Category.id)
            .join(
                models.Transaction,
                models.Object.transaction_id == models.Transaction.id,
            )
            .outerjoin(comments_subq, models.Object.id == comments_subq.c.object_id)
            .order_by(models.Object.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        stmt = self.make_filters(filters=filters, stmt=stmt)

        return list((await self.session.execute(stmt)).mappings().all())

    async def get_object(
        self,
        *,
        obj: models.Object,
    ) -> RowMapping:
        """Возвращает список объектов с пагинацией.

        Возвращает список объектов с пагинацией фильтром по категории,
        отсортированных по created_at DESC, с числом комментариев.
        """
        # Подзапрос для подсчёта комментариев
        comments_count_subq = (
            select(func.count(models.Comment.id))
            .where(models.Comment.object_id == models.Object.id)
            .scalar_subquery()
        )

        stmt = (
            select(
                models.Object,
                models.User,
                models.City,
                models.Category,
                models.Transaction,
                func.coalesce(comments_count_subq, 0).label("comments_count"),
            )
            .where(models.Object.id == obj.id)
            .join(models.User, models.Object.user_id == models.User.id)
            .join(models.City, models.Object.city_id == models.City.id)
            .join(models.Category, models.Object.category_id == models.Category.id)
            .join(
                models.Transaction,
                models.Object.transaction_id == models.Transaction.id,
            )
        )

        return (await self.session.execute(stmt)).mappings().one()

    async def get_object_by_id(self, object_id: int) -> models.Object | NoResultFound:
        """Получить объект по ID.

        :param object_id: _description_
        :type object_id: int
        :return: _description_
        :rtype: models.Object | NoResultFound
        """
        stmt = select(models.Object).where(models.Object.id == object_id)
        return (await self.session.execute(stmt)).scalar_one()

    def make_filters(
        self, *, filters: dict[str, str] | None = None, stmt: Select[Any]
    ) -> Select[Any]:
        if filters is not None:
            if filters.get("category_id") is not None:
                stmt = stmt.where(
                    models.Object.category_id == filters.get("category_id")
                )
        return stmt
