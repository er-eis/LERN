import logging
import time
from datetime import datetime

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

import environment
from ml_models.registry import ML_MODELS
from models.db.base import Base
from models.db.command import Command
from models.db.mlmodel import MLModel
from models.db.user import User

logger = logging.getLogger(__name__)


engine = create_engine(
    f"postgresql+psycopg2://{environment.DB_USER}:{environment.DB_PASS}@{environment.DB_HOST}:{environment.DB_PORT}/{environment.DB_NAME}"
)
Base.metadata.create_all(engine)


def _main_execute_loop():
    waits = 0
    while True:
        while True:
            with Session(engine) as session:
                with session.begin():
                    statement_oldest_command = (
                        select(Command)
                        .select_from(Command)
                        .where(Command.executed_at.is_(None))
                        .order_by(Command.created_at.asc())
                        .limit(1)
                    )
                    oldest_command_not_executed: Command | None = session.execute(
                        statement_oldest_command
                    ).scalar_one_or_none()
                    if oldest_command_not_executed is None:
                        break

                    statement_all_commands_of_oldest_type = (
                        select(Command)
                        .select_from(Command)
                        .where(
                            Command.ml_model_id
                            == oldest_command_not_executed.ml_model_id,
                            Command.executed_at.is_(None),
                        )
                        .order_by(Command.created_at.asc())
                    )
                    commands_to_execute: list[Command] = session.execute(
                        statement_all_commands_of_oldest_type
                    ).all()

                    ml_model = ML_MODELS[oldest_command_not_executed.ml_model_id]
                for command_row in commands_to_execute:
                    with session.begin():
                        command = command_row[0]
                        result = ml_model.execute(command_text=command.command_text)
                        command.executed_at = datetime.now()
                        session.add(command)
                        logger.info(
                            f"Executed command {command.id} for user {command.user_id}, result: {result}"
                        )

        if waits % 60 == 0:
            logger.info(f"No commands to execute. Waiting...")
        waits += 1
        time.sleep(3)


def _get_ml_models():
    with Session(engine) as session:
        ml_models = session.query(MLModel).all()
    return ml_models


def _insert_ml_model_command(ml_model_id: int, command_text: str, user_uid: str):
    with Session(engine) as session:
        with session.begin():
            user = session.query(User).filter(User.uid == user_uid).one_or_none()
            command = Command(
                ml_model_id=ml_model_id,
                command_text=command_text,
                user_id=user.id,
            )
            session.add(command)
        result_str = f"Queued {command} for {user_uid}"
    return result_str