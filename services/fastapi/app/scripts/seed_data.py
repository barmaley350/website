import random

import typer
from faker import Faker
from sqlalchemy.orm import Session

from app.db.db import Base, SessionLocal, engine
from app.models import Comment, Post, User

app = typer.Typer()
fake = Faker("ru_RU")


def process(i: int, model: str) -> None:
    print(f"\rСоздано {model} - {i}", end="")


@app.command()
def seed(
    count_users: int = typer.Option(
        10, "--users", "-u", help="Количество пользователей"
    ),
    count_posts: int = typer.Option(50, "--posts", "-p", help="Количество постов"),
    count_comments: int = typer.Option(
        50, "--comments", "-c", help="Количество коментариев"
    ),
    drop_first: bool = typer.Option(
        False, "--drop", help="Очистить таблицы перед заполнением"
    ),
):

    if drop_first:
        typer.echo("Очистка таблиц...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        # Создаём пользователей
        users = []
        for i in range(count_users):
            user = User(
                username=fake.name(),
                email=fake.email(),
                is_active=True,
            )
            # session.add(user)
            users.append(user)
            process(i + 1, "User")
        session.add_all(users)
        session.commit()  # чтобы получить id
        print()

        # Создаём товары, привязывая к пользователям
        posts = []
        for i in range(count_posts):
            owner = users[random.randint(0, len(users) - 1)]  # noqa: S311
            date = fake.date_time_between(start_date="-1y", end_date="now")
            post = Post(
                title=fake.text(100),
                content=fake.text(),
                user_id=owner.id,
                created_at=date,
            )
            posts.append(post)
            # session.add(post)
            process(i + 1, "Post")
        session.add_all(posts)
        session.commit()
        print()

        comments = []
        comments_count = 0
        for post in random.sample(posts, len(posts) // 3):
            for _ in range(random.randint(1, count_comments)):  # noqa: S311
                owner = users[random.randint(0, len(users) - 1)]  # noqa: S311
                date = fake.date_time_between(
                    start_date=post.created_at, end_date="now"
                )
                comments.append({
                    "content": fake.text(100),
                    "user_id": owner.id,
                    "post_id": post.id,
                    "created_at": date,
                })
                comments_count += 1
                process(comments_count, "Comment")

        session.bulk_insert_mappings(Comment, comments)  # type: ignore
        session.commit()
        print()
        typer.echo("\nГотово!")


if __name__ == "__main__":
    app()
