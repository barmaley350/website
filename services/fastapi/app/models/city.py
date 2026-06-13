from sqlalchemy import Boolean, Column, Integer, String

from app.db.db import Base


# Коммерческая недвижимость, Земельные участки, Готовый бизнес, Виллы
class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
