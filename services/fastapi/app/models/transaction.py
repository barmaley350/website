from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


# продам, сдам
class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


# from sqlalchemy import Boolean, Column, Integer, String

# from app.db.db import Base


# # продам, сдам
# class Transaction(Base):
#     __tablename__ = "transaction"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)
