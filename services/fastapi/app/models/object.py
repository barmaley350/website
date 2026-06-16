from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.db.db import Base


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
    user: Mapped["models.User"] = relationship("User", backref="objects")
    category: Mapped["models.Category"] = relationship("Category", backref="objects")
    city: Mapped["models.City"] = relationship("City", backref="objects")
    transaction: Mapped["models.Transaction"] = relationship(
        "Transaction", backref="objects"
    )


# from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

# from app.db.db import Base


# class Object(Base):
#     __tablename__ = "object"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=False)
#     price = Column(Integer, nullable=False)
#     is_active = Column(Boolean, default=True)
#     category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
#     transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=True)
#     city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     created_at = Column(DateTime, nullable=True)

#     user = relationship("User", backref="objects")
#     category = relationship("Category", backref="objects")
#     city = relationship("City", backref="objects")
#     transaction = relationship("Transaction", backref="objects")
