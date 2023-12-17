import time

from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import environment
from models.base import Base
from models.command import Command
from models.mlmodel import MLModel

app = FastAPI()
engine = create_engine(
    f"postgresql+psycopg2://{environment.DB_USER}:{environment.DB_PASS}@{environment.DB_HOST}:{environment.DB_PORT}/{environment.DB_NAME}"
)
Base.metadata.create_all(engine)


@app.on_event("startup")
async def app_startup():
    while True:
        while True:
            with Session(engine) as session:
                statement_oldest_command = (
                    select(Command)
                    .select_from(Command)
                    .where(Command.executed_at.is_(None))
                    .order_by(Command.created_at.asc())
                    .limit(1)
                )
                oldest_command_not_executed: Command | None = session.execute(
                    statement_oldest_command
                ).one_or_none()
                if oldest_command_not_executed is None:
                    break

                statement_all_commands_of_oldest_type = (
                    select(Command.command_text, Command.user_id)
                    .select_from(Command)
                    .where(
                        Command.ml_model_id == oldest_command_not_executed.ml_model_id
                    )
                    .order_by(Command.created_at.asc())
                )
                commands_to_execute: list[tuple[str, int]] = session.execute(
                    statement_all_commands_of_oldest_type
                ).all()

        print("Waiting for a command...")
        time.sleep(3)


@app.get("/mlmodels")
def read_mlmodels():
    with Session(engine) as session:
        ml_models = session.query(MLModel).all()
        return ml_models
