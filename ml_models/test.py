from models.db.mlmodel import MLModel, Encoding


class Test(MLModel):
    @staticmethod
    def execute(command_text: str) -> tuple[bytes, Encoding.UTF_8]:
        return f"Executed {command_text}".encode(Encoding.UTF_8.value), Encoding.UTF_8
