from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.apps.category.models import Category
    from app.apps.city.models import City
    from app.apps.transaction.models import Transaction
    from app.apps.user.models import User
from app.core.settings import Base


class Object(Base):
    __tablename__ = "object"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), nullable=False
    )
    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("transaction.id"), nullable=False
    )
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("city.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # Связи
    user: Mapped["User"] = relationship("User", backref="objects")
    category: Mapped["Category"] = relationship("Category", backref="objects")
    city: Mapped["City"] = relationship("City", backref="objects")
    transaction: Mapped["Transaction"] = relationship("Transaction", backref="objects")
