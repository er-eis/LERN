from sqlalchemy import TEXT, BOOLEAN, Column
from sqlalchemy.orm import relationship

from models.base import CommonColumns


class User(CommonColumns):
    __tablename__ = "users"

    name = Column(TEXT, nullable=False)
    admin = Column(BOOLEAN, nullable=False, default=False, server_default="False")
    location = relationship("Location", back_populates="user")
    command = relationship("Command", back_populates="user")
