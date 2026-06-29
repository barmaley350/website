from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings import Base


class Geo(Base):
    __tablename__ = "geo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
