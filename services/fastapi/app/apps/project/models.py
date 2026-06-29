from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings import Base

if TYPE_CHECKING:
    from app.apps.models import Category, Geo, ProjectSkill, User


# class ProjectSkill(Base):
#     __tablename__ = "project_skills"
#     project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
#     skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

#     project: Mapped["Project"] = relationship(back_populates="project_skills")
#     skill: Mapped["Skill"] = relationship(back_populates="project_skills")


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

    project_skills: Mapped[list[ProjectSkill]] = relationship(back_populates="project")
    skills = association_proxy("project_skills", "project_skills")

    # Связи
    user: Mapped[User] = relationship("User", backref="projects")
    category: Mapped[Category] = relationship("Category", backref="projects")
    geo: Mapped[Geo] = relationship("Geo", backref="projects")
