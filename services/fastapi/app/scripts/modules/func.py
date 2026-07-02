import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

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


def process(i: int, model: str) -> None:
    print(f"\rСоздано {model} - {i}", end="")


async def create_categories(session: AsyncSession, fake: Faker) -> list[Category]:
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
    return categories


async def create_skills(session: AsyncSession, fake: Faker) -> list[Skill]:
    skills_data = ["python3", "sql", "clickhouse", "fastapi"]
    skills = [Skill(name=name) for name in skills_data]
    session.add_all(skills)
    await session.commit()
    return skills


async def create_geos(session: AsyncSession, fake: Faker) -> list[Geo]:
    geos_data = [
        "Москва",
        "РФ",
        "Мир",
        "Санкт-Петербург",
    ]
    geos = [Geo(name=name) for name in geos_data]
    session.add_all(geos)
    await session.commit()
    return geos


async def create_users(
    session: AsyncSession, fake: Faker, count_users: int
) -> list[User]:
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
    return users


async def create_user_skills(
    session: AsyncSession, users: list[User], skills: list[Skill]
) -> list[UserSkill]:
    user_skills_objects = []
    for user in users:
        num_skills = random.randint(1, len(skills))
        chosen_skills = random.sample(skills, num_skills)
        for skill in chosen_skills:
            user_skill = UserSkill(user_id=user.id, skill_id=skill.id)
            user_skills_objects.append(user_skill)
        process(len(user_skills_objects), "UserSkill")
    session.add_all(user_skills_objects)
    await session.commit()
    print()
    return user_skills_objects


async def create_projects(
    session: AsyncSession,
    fake: Faker,
    count_projects: int,
    categories: list[Category],
    geos: list[Geo],
    users: list[User],
) -> list[Project]:
    pass
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
    return projects


async def create_project_skills(
    session: AsyncSession, projects: list[Project], skills: list[Skill]
) -> list[ProjectSkill]:
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

    return project_skills_objects


async def create_project_teams(
    session: AsyncSession, projects: list[Project], users: list[User]
) -> list[ProjectTeam]:
    project_teams_objects = []
    for project in projects:
        num_teams = random.randint(1, 7)
        chosen_users = random.sample(users, num_teams)
        for user in chosen_users:
            project_team = ProjectTeam(project_id=project.id, user_id=user.id)
            project_teams_objects.append(project_team)
        process(len(project_teams_objects), "ProjectTeam")
    session.add_all(project_teams_objects)
    await session.commit()
    print()
    return project_teams_objects


async def create_projects_comments(
    session: AsyncSession,
    fake: Faker,
    projects: list[Project],
    users: list[User],
    count_comments: int,
) -> None:
    comments_data_list = []
    comments_count = 0
    sample_size = max(1, len(projects) // 3)

    sampled_projects = random.sample(projects, sample_size)

    for project in sampled_projects:
        for _ in range(random.randint(1, count_comments)):
            owner = users[random.randint(0, len(users) - 1)]
            date = fake.date_time_between(start_date=project.created_at, end_date="now")  # type: ignore

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
