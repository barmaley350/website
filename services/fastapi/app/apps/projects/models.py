from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings import Base

if TYPE_CHECKING:
    from app.apps.models import Category, Geo, ProjectSkill, User


class ProjectTeam(Base):
    __tablename__ = "project_teams"
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    # Связи к основным сущностям
    user: Mapped[User] = relationship(back_populates="teams")
    project: Mapped[Project] = relationship(back_populates="teams")


# FIX description_full -> False
class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    description_full: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), nullable=False
    )
    geo_id: Mapped[int] = mapped_column(Integer, ForeignKey("geo.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    skills: Mapped[list[ProjectSkill]] = relationship(back_populates="project")
    # skills = association_proxy("project_skills", "skill")
    teams: Mapped[list[ProjectTeam]] = relationship(back_populates="project")

    # Связи
    user: Mapped[User] = relationship("User", backref="projects")
    category: Mapped[Category] = relationship("Category", backref="projects")
    geo: Mapped[Geo] = relationship("Geo", backref="projects")
