from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.apps.project.models import Project
    from app.apps.user.models import User
from app.core.settings import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # Связи
    object: Mapped["Project"] = relationship("Project", backref="comments")
    user: Mapped["User"] = relationship("User", backref="comments")
