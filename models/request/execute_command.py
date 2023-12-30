from pydantic import BaseModel


class PostExecuteCommand(BaseModel):
    uid: str
    command_text: str
    ml_model_id: int
    channel_id: str
    message_id: str


class TurnOnOrOff(BaseModel):
    uid: str
