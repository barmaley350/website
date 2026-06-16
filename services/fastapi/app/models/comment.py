from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.db.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    object_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("object.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # Связи
    object: Mapped["models.Object"] = relationship("Object", backref="comments")
    user: Mapped["models.User"] = relationship("User", backref="comments")


# from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
# from sqlalchemy.orm import relationship

# from app.db.db import Base


# # TODO Добавить nullable=False к created_at
# # Сейчас такое настройки для только что бы работала генерация fake данных
# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(Text, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     object_id = Column(Integer, ForeignKey("object.id"), nullable=False)
#     created_at = Column(DateTime, nullable=True)

#     object = relationship("Object", backref="comments")
#     user = relationship("User", backref="comments")
