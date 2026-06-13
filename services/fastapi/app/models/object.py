from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.db import Base


class Object(Base):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=True)

    user = relationship("User", backref="objects")
    category = relationship("Category", backref="objects")
    city = relationship("City", backref="objects")
    transaction = relationship("Transaction", backref="objects")
