from sqlalchemy import Boolean, Column, Integer, String

from app.db.db import Base


# продам, сдам
class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
