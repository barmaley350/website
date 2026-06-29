import asyncio
import random
from contextlib import asynccontextmanager

import typer
from faker import Faker

from app.apps.models import (
    Category,
    Comment,
    Geo,
    Project,
    ProjectSkill,
    ProjectTeam,
    Skill,
    User,
    UserSkill,
)
from app.core.dependencies import db
from app.core.settings import Base


@asynccontextmanager
async def get_session():
    async with db.db_session() as session:
        yield session


app = typer.Typer()
fake = Faker("ru_RU")


def process(i: int, model: str) -> None:
    print(f"\rСоздано {model} - {i}", end="")


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
        # --- 1. Categories ---
        categories_data = [
            "Коммерческая недвижимость",
            "Земельные участки",
            "Готовый бизнес",
            "Виллы",
        ]
        categories = [
            Category(name=name, description=fake.text(100)) for name in categories_data
        ]
        session.add_all(categories)
        await session.commit()

        # --- 2. Skills ---
        skills_data = ["python3", "sql", "clickhouse", "fastapi"]
        skills = [Skill(name=name) for name in skills_data]
        session.add_all(skills)
        await session.commit()

        # --- 3. Cities ---
        geos_data = [
            "Москва",
            "РФ",
            "Мир",
            "Санкт-Петербург",
        ]
        geos = [Geo(name=name) for name in geos_data]
        session.add_all(geos)
        await session.commit()

        # --- 4. Users ---
        users = []
        for i in range(count_users):
            user = User(
                username=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                is_active=True,
            )
            users.append(user)
            process(i + 1, "User")

        session.add_all(users)
        await session.commit()
        print()

        # --- User Skills ---
        user_skills_objects = []
        for user in users:
            # каждый пользователь получает случайное количество навыков от 1 до len(skills)
            num_skills = random.randint(1, len(skills))
            chosen_skills = random.sample(skills, num_skills)
            for skill in chosen_skills:
                user_skill = UserSkill(user_id=user.id, skill_id=skill.id)
                user_skills_objects.append(user_skill)
            process(len(user_skills_objects), "UserSkill")
        session.add_all(user_skills_objects)
        await session.commit()
        print()

        # --- 5. Objects ---
        projects = []
        for i in range(count_projects):
            date = fake.date_time_between(start_date="-1y", end_date="now")
            project = Project(
                title=fake.text(100),
                description=fake.text(1000),
                is_active=True,
                category_id=categories[random.randint(0, len(categories) - 1)].id,
                geo_id=geos[random.randint(0, len(geos) - 1)].id,
                user_id=users[random.randint(0, len(users) - 1)].id,
                created_at=date,
            )
            projects.append(project)
            process(i + 1, "Project")

        session.add_all(projects)
        await session.commit()
        print()

        # --- Project Skills ---
        project_skills_objects = []
        for project in projects:
            # каждый пользователь получает случайное количество навыков от 1 до len(skills)
            num_skills = random.randint(1, len(skills))
            chosen_skills = random.sample(skills, num_skills)
            for skill in chosen_skills:
                project_skill = ProjectSkill(project_id=project.id, skill_id=skill.id)
                project_skills_objects.append(project_skill)
            process(len(project_skills_objects), "ProjectSkill")
        session.add_all(project_skills_objects)
        await session.commit()
        print()

        # --- Project Teams ---
        project_teams_objects = []
        for project in projects:
            # каждый пользователь получает случайное количество навыков от 1 до len(skills)
            # len_user = len(users) if len(users) <= 5 else 5
            num_teams = random.randint(1, 7)
            chosen_users = random.sample(users, num_teams)
            for user in chosen_users:
                project_team = ProjectTeam(project_id=project.id, user_id=user.id)
                project_teams_objects.append(project_team)
            process(len(project_teams_objects), "ProjectTeam")
        session.add_all(project_teams_objects)
        await session.commit()
        print()

        # --- 6. Comments ---
        comments_data_list = []
        comments_count = 0
        sample_size = max(1, len(projects) // 3)

        sampled_projects = random.sample(projects, sample_size)

        for project in sampled_projects:
            for _ in range(random.randint(1, count_comments)):
                owner = users[random.randint(0, len(users) - 1)]
                date = fake.date_time_between(
                    start_date=project.created_at, end_date="now"
                )

                comments_data_list.append({
                    "content": fake.text(100),
                    "user_id": owner.id,
                    "project_id": project.id,
                    "created_at": date,
                })
                comments_count += 1
                process(comments_count, "Comment")

        if comments_data_list:
            comment_objects = [Comment(**data) for data in comments_data_list]
            session.add_all(comment_objects)
            await session.commit()

        print()
        typer.echo("\nГотово!")


if __name__ == "__main__":
    app()
