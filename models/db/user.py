from sqlalchemy import TEXT, BOOLEAN, Column
from sqlalchemy.orm import relationship

from models.db.base import CommonColumns


class User(CommonColumns):
    __tablename__ = "users"

    name = Column(TEXT, nullable=False)
    uid = Column(TEXT, nullable=False)
    admin = Column(BOOLEAN, nullable=False, default=False, server_default="False")
    commands = relationship("Command", back_populates="user")
