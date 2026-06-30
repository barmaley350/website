from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps import models


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_comments_count(self, project_id: int) -> int:
        """Количество комментариев к объекту."""
        stmt = select(func.count(models.Comment.id)).where(
            models.Comment.project_id == project_id
        )
        return (await self.session.execute(stmt)).scalar() or 0

    async def get_similar_projects(
        self,
        obj: models.Project,
        limit: int = 3,
    ):
        """Похожие объекты (по городу, категории, транзакции, исключая текущий)."""
        comments_subq = (
            select(
                models.Comment.project_id, func.count(models.Comment.id).label("cnt")
            )
            .group_by(models.Comment.project_id)
            .subquery()
        )

        # Основной запрос с выбором всех нужных полей
        stmt = (
            select(
                models.Project,
                models.User,
                models.Geo,
                models.Category,
                func.coalesce(comments_subq.c.cnt, 0).label("comments_count"),
            )
            .join(models.User, models.Project.user_id == models.User.id)
            .join(models.Geo, models.Project.geo_id == models.Geo.id)
            .join(models.Category, models.Project.category_id == models.Category.id)
            .outerjoin(comments_subq, models.Project.id == comments_subq.c.project_id)
            .where(
                models.Project.geo_id == obj.geo_id,
                models.Project.category_id == obj.category_id,
                models.Project.id != obj.id,  # исключаем текущий объект
            )
            .limit(limit)
            .order_by(models.Project.created_at.desc())
        )

        return list((await self.session.execute(stmt)).mappings().all())

    async def get_projects_count(self, filters: dict[str, str] | None = None) -> int:
        """Общее количество объектов (с фильтром по категории, если указан)."""
        stmt = select(func.count(models.Project.id))
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

    async def get_projects(
        self,
        *,
        filters: dict[str, str],
        offset: int = 0,
        limit: int = 10,
    ):  # -> list[RowMapping]:
        """Возвращает список объектов с пагинацией.

        Возвращает список объектов с пагинацией фильтром по категории,
        отсортированных по created_at DESC, с числом комментариев.
        """
        # Подзапрос для подсчёта комментариев
        comments_subq = (
            select(
                models.Comment.project_id, func.count(models.Comment.id).label("cnt")
            )
            .group_by(models.Comment.project_id)
            .subquery()
        )

        # --- ПОДЗАПРОС ДЛЯ НАВЫКОВ ---
        user_skills_subq = (
            select(
                models.UserSkill.user_id,
                func.array_agg(models.Skill.name).label("user_skills"),
            )
            .join(models.Skill, models.UserSkill.skill_id == models.Skill.id)
            .group_by(models.UserSkill.user_id)
            .subquery()
        )
        # --- ПОДЗАПРОС ДЛЯ НАВЫКОВ ---
        project_skills_subq = (
            select(
                models.ProjectSkill.project_id,
                func.array_agg(models.Skill.name).label("project_skills"),
            )
            .join(models.Skill, models.ProjectSkill.skill_id == models.Skill.id)
            .group_by(models.ProjectSkill.project_id)
            .subquery()
        )
        stmt = (
            select(
                models.Project,
                models.User,
                models.Geo,
                models.Category,
                func.coalesce(comments_subq.c.cnt, 0).label("comments_count"),
                func.coalesce(user_skills_subq.c.user_skills, []).label("user_skills"),
                func.coalesce(project_skills_subq.c.project_skills, []).label(
                    "project_skills"
                ),
            )
            .join(models.User, models.Project.user_id == models.User.id)
            .join(models.Geo, models.Project.geo_id == models.Geo.id)
            .join(models.Category, models.Project.category_id == models.Category.id)
            .outerjoin(comments_subq, models.Project.id == comments_subq.c.project_id)
            .outerjoin(user_skills_subq, models.User.id == user_skills_subq.c.user_id)
            .outerjoin(
                project_skills_subq,
                models.Project.id == project_skills_subq.c.project_id,
            )
            .order_by(models.Project.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        stmt = self.make_filters(filters=filters, stmt=stmt)
        rows = list((await self.session.execute(stmt)).mappings().all())

        # ---------
        # 2. Загружаем пользователей команды для всех проектов
        if not rows:
            return rows

        result_rows = [dict(row) for row in rows]
        project_ids = [row["Project"].id for row in rows]
        team_stmt = (
            select(
                models.ProjectTeam.project_id,
                models.User,
            )
            .join(models.User, models.ProjectTeam.user_id == models.User.id)
            .where(models.ProjectTeam.project_id.in_(project_ids))
        )
        team_result = await self.session.execute(team_stmt)

        # Группируем пользователей по project_id
        team_users_map: dict[int, list[models.User]] = {}
        for project_id, user in team_result:
            team_users_map.setdefault(project_id, []).append(user)

        # 3. Добавляем team_users в каждую строку
        for row_dict in result_rows:
            project_id = row_dict["Project"].id
            users = team_users_map.get(project_id, [])
            row_dict["team_users"] = users  # теперь можно присваивать

        return result_rows

    async def get_project(
        self,
        *,
        obj: models.Project,
    ) -> RowMapping:
        """Возвращает список объектов с пагинацией.

        Возвращает список объектов с пагинацией фильтром по категории,
        отсортированных по created_at DESC, с числом комментариев.
        """
        # Подзапрос для подсчёта комментариев
        comments_count_subq = (
            select(func.count(models.Comment.id))
            .where(models.Comment.project_id == models.Project.id)
            .scalar_subquery()
        )

        stmt = (
            select(
                models.Project,
                models.User,
                models.Geo,
                models.Category,
                func.coalesce(comments_count_subq, 0).label("comments_count"),
            )
            .where(models.Project.id == obj.id)
            .join(models.User, models.Project.user_id == models.User.id)
            .join(models.Geo, models.Project.geo_id == models.Geo.id)
            .join(models.Category, models.Project.category_id == models.Category.id)
        )

        return (await self.session.execute(stmt)).mappings().one()

    async def get_project_by_id(
        self, project_slug: str
    ) -> models.Project | NoResultFound:
        stmt = select(models.Project).where(models.Project.slug == project_slug)
        return (await self.session.execute(stmt)).scalar_one()

    def make_filters(
        self, *, filters: dict[str, str] | None = None, stmt: Select[Any]
    ) -> Select[Any]:
        if filters is not None:
            if filters.get("category_id") is not None:
                stmt = stmt.where(
                    models.Project.category_id == filters.get("category_id")
                )
        return stmt
