from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    post = relationship("Post", backref="comments")
