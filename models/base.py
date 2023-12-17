from sqlalchemy import Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CommonColumns(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
