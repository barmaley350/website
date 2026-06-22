from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings import Base


# Коммерческая недвижимость, Земельные участки, Готовый бизнес, Виллы
class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


# from sqlalchemy import Boolean, Column, Integer, String

# from app.db.db import Base


# # Коммерческая недвижимость, Земельные участки, Готовый бизнес, Виллы
# class City(Base):
#     __tablename__ = "city"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)
