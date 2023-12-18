import logging
import threading

from fastapi import FastAPI

from helpers import (
    _main_ml_model_execute_loop,
    _get_ml_models,
    _insert_ml_model_command,
    _turn_execution_on_or_off,
)
from models.request.execute_command import PostExecuteCommand, TurnOnOrOff
from utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
def app_startup():
    threading.Thread(target=_main_ml_model_execute_loop).start()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/mlmodels")
def read_mlmodels():
    ml_models = _get_ml_models()
    return ml_models


@app.post("/mlmodels/execute")
def execute_command(command: PostExecuteCommand):
    queued_command_result = _insert_ml_model_command(
        ml_model_id=command.ml_model_id,
        command_text=command.command_text,
        user_uid=command.uid,
    )
    return queued_command_result


@app.put("/mlmodels/execute")
def turn_execution_on_or_off(turn_on_or_off: TurnOnOrOff):
    result = _turn_execution_on_or_off(
        user_uid=turn_on_or_off.uid,
    )
    return result
