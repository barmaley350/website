import asyncio
from contextlib import asynccontextmanager

import typer
from faker import Faker

from app.core.dependencies import db
from app.core.settings import Base

from .modules import func


@asynccontextmanager
async def get_session():
    async with db.db_session() as session:
        yield session


app = typer.Typer()
fake = Faker("ru_RU")


# Синхронная команда Typer – она просто запускает асинхронную логику
@app.command()
def seed(
    count_users: int = typer.Option(
        10, "--users", "-u", help="Количество пользователей"
    ),
    count_projects: int = typer.Option(
        50, "--projects", "-p", help="Количество проектов"
    ),
    count_comments: int = typer.Option(
        50, "--comments", "-c", help="Количество комментариев"
    ),
    drop_first: bool = typer.Option(
        False,
        "--drop",
        help="Очистить таблицы перед заполнением",
        show_default=True,
    ),
):
    asyncio.run(async_seed(count_users, count_projects, count_comments, drop_first))


# Вся асинхронная работа здесь
async def async_seed(
    count_users: int,
    count_projects: int,
    count_comments: int,
    drop_first: bool,
):
    engine = db.db_engine

    if drop_first:
        if not typer.confirm(
            "⚠️ ВНИМАНИЕ: Это удалит ВСЕ таблицы в текущей БД! Продолжить?", abort=True
        ):
            return
        typer.echo("Очистка и пересоздание таблиц...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async with get_session() as session:
        categories = await func.create_categories(session, fake)
        skills = await func.create_skills(session, fake)
        geos = await func.create_geos(session, fake)
        users = await func.create_users(session, fake, count_users)
        users_skills = await func.create_user_skills(session, users, skills)
        projects = await func.create_projects(
            session, fake, count_projects, categories, geos, users
        )
        projects_skills = await func.create_project_skills(session, projects, skills)
        projects_teams = await func.create_project_teams(session, projects, users)
        await func.create_projects_comments(
            session, fake, projects, users, count_comments
        )
        typer.echo("\nГотово!")


if __name__ == "__main__":
    app()
