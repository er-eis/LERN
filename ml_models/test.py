from models.db.mlmodel import MLModel, MLEncodingEnum


class Test(MLModel):
    def __init__(self, *args, **kwargs):
        pass

    def execute(self, command_text: str) -> tuple[bytes, MLEncodingEnum.UTF_8]:
        return (
            f"Executed {command_text}".encode(MLEncodingEnum.UTF_8.value),
            MLEncodingEnum.UTF_8,
        )
