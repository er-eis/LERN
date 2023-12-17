from sqlalchemy import Column, INTEGER, ForeignKey, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from models.db.base import CommonColumns
from models.db.mlmodel import MLEncodingEnum


class Result(CommonColumns):
    __tablename__ = "results"

    command_id = Column(INTEGER, ForeignKey("commands.id"), nullable=False)
    command = relationship("Command", back_populates="result")
    output = Column(LargeBinary, nullable=True)
    encoding = Column(ENUM(MLEncodingEnum, name="ml_encoding"), nullable=False)
    sent_at = Column(
        DateTime(timezone=True), nullable=True, default=None, server_default=None
    )

    def __repr__(self):
        return f"<Result {self.id} (command_id={self.command_id}, encoding='{self.encoding}', was_sent={self.sent_at is not None}, output='{self.output[:15]}'...)>"
