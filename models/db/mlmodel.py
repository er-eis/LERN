from abc import abstractmethod
from enum import Enum

from sqlalchemy import TEXT, Column, BOOLEAN
from sqlalchemy.orm import relationship

from models.db.base import CommonColumns


class MLEncodingEnum(Enum):
    UTF_8 = "utf-8"
    BASE_64 = "base64"


class MLModel(CommonColumns):
    __tablename__ = "ml_models"

    name = Column(TEXT, nullable=False)
    location = Column(TEXT, nullable=False)
    admin_only = Column(BOOLEAN, nullable=False, default=True, server_default="True")
    commands = relationship("Command", back_populates="ml_model")

    @abstractmethod
    def __init__(self, location: str, *args, **kwargs):
        pass

    @abstractmethod
    def execute(self, command_text: str) -> tuple[bytes, MLEncodingEnum]:
        pass

    def __repr__(self):
        return f"<MLModel {self.id} (name={self.name}, admin_only={self.admin_only}, created_at={self.created_at.isoformat()}>"
