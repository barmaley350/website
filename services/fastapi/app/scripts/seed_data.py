import asyncio
import random
from contextlib import asynccontextmanager

import typer
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.models import Category, City, Comment, Object, Transaction, User
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
    count_obj: int = typer.Option(50, "--obj", "-o", help="Количество объектов"),
    count_comments: int = typer.Option(
        50, "--comments", "-c", help="Количество комментариев"
    ),
    drop_first: bool = typer.Option(
        False, "--drop", help="Очистить таблицы перед заполнением"
    ),
):
    asyncio.run(async_seed(count_users, count_obj, count_comments, drop_first))


# Вся асинхронная работа здесь
async def async_seed(
    count_users: int,
    count_obj: int,
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
            Category(title=title, description=fake.text(100))
            for title in categories_data
        ]
        session.add_all(categories)
        await session.commit()

        # --- 2. Transactions ---
        transactions_data = ["Продам", "Сдам"]
        transactions = [
            Transaction(title=t, description=fake.text(100)) for t in transactions_data
        ]
        session.add_all(transactions)
        await session.commit()

        # --- 3. Cities ---
        cities_data = [
            "Thalang",
            "Вичит",
            "Карон (Karon)",
            "Кату (Kathu)",
            "Ко Каев (Ko Kaeo)",
            "Патонг (Patong)",
            "Раваи (Rawai)",
            "Талат Нуэа",
            "Талат Яй",
            "Тхаланг",
            "Чалонг (Chalong)",
        ]
        cities = [City(title=c, description=fake.text(100)) for c in cities_data]
        session.add_all(cities)
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

        # --- 5. Objects ---
        objs = []
        for i in range(count_obj):
            date = fake.date_time_between(start_date="-1y", end_date="now")
            obj = Object(
                title=fake.text(100),
                description=fake.text(1000),
                price=random.randint(10000, 1000000),
                is_active=True,
                category_id=categories[random.randint(0, len(categories) - 1)].id,
                city_id=cities[random.randint(0, len(cities) - 1)].id,
                user_id=users[random.randint(0, len(users) - 1)].id,
                transaction_id=transactions[
                    random.randint(0, len(transactions) - 1)
                ].id,
                created_at=date,
            )
            objs.append(obj)
            process(i + 1, "Object")

        session.add_all(objs)
        await session.commit()
        print()

        # --- 6. Comments ---
        comments_data_list = []
        comments_count = 0
        sample_size = max(1, len(objs) // 3)

        sampled_objs = random.sample(objs, sample_size)

        for obj in sampled_objs:
            for _ in range(random.randint(1, count_comments)):
                owner = users[random.randint(0, len(users) - 1)]
                date = fake.date_time_between(start_date=obj.created_at, end_date="now")

                comments_data_list.append({
                    "content": fake.text(100),
                    "user_id": owner.id,
                    "object_id": obj.id,
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
