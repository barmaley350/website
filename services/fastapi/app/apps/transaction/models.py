from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings import Base


# продам, сдам
class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

