from sqlalchemy import Boolean, Column, Integer, String

from app.db.db import Base


# Коммерческая недвижимость, Земельные участки, Готовый бизнес, Виллы
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
