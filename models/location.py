from sqlalchemy import TEXT, Column, ForeignKey, INTEGER

from models.base import CommonColumns


class Location(CommonColumns):
    __tablename__ = "locations"

    name = Column(TEXT, nullable=False)
    identifier = Column(TEXT, nullable=False)
    user_id = Column(INTEGER, ForeignKey("users.id"))
