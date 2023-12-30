from sqlalchemy import Column, TEXT, INTEGER, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models.db.base import CommonColumns


class Command(CommonColumns):
    __tablename__ = "commands"

    command_text = Column(TEXT, nullable=False)
    user_id = Column(INTEGER, ForeignKey("users.id"))
    ml_model_id = Column(INTEGER, ForeignKey("ml_models.id"))
    ml_model = relationship("MLModel", back_populates="commands")
    user = relationship("User", back_populates="commands")
    executed_at = Column(DateTime(timezone=True), nullable=True, default=None)
    result = relationship("Result", back_populates="command")
    channel_id = Column(TEXT, nullable=True, default=None)
    message_id = Column(TEXT, nullable=True, default=None)

    def __repr__(self):
        return f"<Command {self.id} (user={self.user_id}, ml_model={self.ml_model_id}, command_text='{self.command_text[:15]}'...)>"
