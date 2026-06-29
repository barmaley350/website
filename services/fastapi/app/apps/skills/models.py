from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.apps.models import Project, User

from app.core.settings import Base


class UserSkill(Base):
    __tablename__ = "user_skills"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

    # Связи к основным сущностям
    user: Mapped[User] = relationship(back_populates="user_skills")
    skill: Mapped[Skill] = relationship(back_populates="user_skills")


class ProjectSkill(Base):
    __tablename__ = "project_skills"
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

    project: Mapped[Project] = relationship(back_populates="project_skills")
    skill: Mapped[Skill] = relationship(back_populates="project_skills")


# FIX name должен быть nullable=False
# Указано True только при создании демо данных
class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True, index=True)

    user_skills: Mapped[list[UserSkill]] = relationship(back_populates="skill")
    users = association_proxy("user_skills", "user")

    project_skills: Mapped[list[ProjectSkill]] = relationship(back_populates="skill")
    projects = association_proxy("project_skills", "project")
