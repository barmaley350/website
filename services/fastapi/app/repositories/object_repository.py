from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class ObjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_object_with_relations(
        self, object_id: int
    ) -> tuple[
        models.Object, models.User, models.City, models.Category, models.Transaction
    ]:
        """Возвращает объект и все связанные сущности.

        Если не найден или найдено несколько — выбрасывает исключения.
        """
        stmt = (
            select(
                models.Object,
                models.User,
                models.City,
                models.Category,
                models.Transaction,
            )
            .join(models.User, models.Object.user_id == models.User.id)
            .join(models.City, models.Object.city_id == models.City.id)
            .join(models.Category, models.Object.category_id == models.Category.id)
            .join(
                models.Transaction,
                models.Object.transaction_id == models.Transaction.id,
            )
            .where(models.Object.id == object_id)
        )

        result = await self.session.execute(stmt)
        obj, user, city, category, transaction = result.one()
        return (obj, user, city, category, transaction)

    async def get_comments_count(self, object_id: int) -> int:
        """Количество комментариев к объекту."""
        stmt = select(func.count(models.Comment.id)).where(
            models.Comment.object_id == object_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def get_similar_objects(
        self,
        object_id: int,
        city_id: int,
        category_id: int,
        transaction_id: int,
        limit: int = 3,
    ) -> list[models.Object]:
        """Похожие объекты (по городу, категории, транзакции, исключая текущий)."""
        stmt = (
            select(models.Object)
            .where(
                models.Object.city_id == city_id,
                models.Object.category_id == category_id,
                models.Object.transaction_id == transaction_id,
                models.Object.id != object_id,
            )
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_objects_count(self, category_id: int | None = None) -> int:
        """Общее количество объектов (с фильтром по категории, если указан)."""
        stmt = select(func.count(models.Object.id))
        if category_id is not None:
            stmt = stmt.where(models.Object.category_id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def get_category_name(self, category_id: int) -> str | None:
        """Название категории по ID."""
        stmt = select(models.Category.title).where(models.Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_objects_with_comments(
        self,
        category_id: int | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[
        tuple[
            models.Object,
            models.User,
            models.City,
            models.Category,
            models.Transaction,
            int,
        ]
    ]:
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

        if category_id is not None:
            stmt = stmt.where(models.Object.category_id == category_id)

        result = await self.session.execute(stmt)
        # return result.all()  # каждый элемент — кортеж из 6 значений
        return [
            (obj, user, city, category, transaction, comments_count)
            for obj, user, city, category, transaction, comments_count in result
        ]
