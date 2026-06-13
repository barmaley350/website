from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.db import Base


# TODO Добавить nullable=False к created_at
# Сейчас такое настройки для только что бы работала генерация fake данных
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    object_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    created_at = Column(DateTime, nullable=True)

    object = relationship("Object", backref="comments")
    user = relationship("User", backref="comments")
