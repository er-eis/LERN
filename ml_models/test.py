from models.mlmodel import MLModel, Encoding


class Test(MLModel):
    def execute(self, command_text: str) -> tuple[bytes, Encoding.UTF_8]:
        return f"Executed {self.command}".encode(Encoding.UTF_8), Encoding.UTF_8
