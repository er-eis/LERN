import enum
from abc import abstractmethod

from sqlalchemy import TEXT, Column, BOOLEAN
from sqlalchemy.orm import relationship

from models.base import CommonColumns


@enum.StrEnum
class Encoding:
    UTF_8 = "utf-8"


class MLModel(CommonColumns):
    __tablename__ = "ml_models"

    name = Column(TEXT, nullable=False)
    location = Column(TEXT, nullable=False)
    admin_only = Column(BOOLEAN, nullable=False, default=True, server_default="True")
    command = relationship("Command", back_populates="mlmodel")

    @abstractmethod
    def execute(self, command_text: str) -> tuple[bytes, Encoding]:
        pass

    def __repr__(self):
        return f"<MLModel {self.id} (name={self.name}, admin_only={self.admin_only}, created_at={self.created_at.isoformat()}>"
