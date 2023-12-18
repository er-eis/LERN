from pydantic import BaseModel


class PostExecuteCommand(BaseModel):
    uid: str
    command_text: str
    ml_model_id: int


class TurnOnOrOff(BaseModel):
    uid: str
