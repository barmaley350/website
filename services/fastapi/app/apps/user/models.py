from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings import Base

if TYPE_CHECKING:
    from app.apps.models import UserSkill


# class UserSkill(Base):
#     __tablename__ = "user_skills"
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
#     skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

#     # Связи к основным сущностям
#     user: Mapped["User"] = relationship(back_populates="user_skills")
#     skill: Mapped["Skill"] = relationship(back_populates="user_skills")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    avatar_github: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_skills: Mapped[list[UserSkill]] = relationship(back_populates="user")
    skills = association_proxy("user_skills", "user_skills")
