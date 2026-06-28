from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.apps.category.models import Category
    from app.apps.geo.models import Geo
    from app.apps.user.models import User
from app.core.settings import Base


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), nullable=False
    )
    geo_id: Mapped[int] = mapped_column(Integer, ForeignKey("geo.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # Связи
    user: Mapped["User"] = relationship("User", backref="projects")
    category: Mapped["Category"] = relationship("Category", backref="projects")
    geo: Mapped["Geo"] = relationship("Geo", backref="projects")
