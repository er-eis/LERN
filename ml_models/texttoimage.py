import torch
import base64
from diffusers import AutoPipelineForText2Image
from io import BytesIO

from models.db.mlmodel import MLModel, MLEncodingEnum


class TextToImage(MLModel):
    def __init__(self, location: str, *args, **kwargs):
        self.location = location
        self.pipeline = AutoPipelineForText2Image.from_pretrained(location, torch_dtype=torch.float16).to('cuda:0')

    def execute(self, command_text: str) -> tuple[bytes, MLEncodingEnum.BASE_64]:
        image = self.pipeline(command_text, temperature=0.9).images[0]
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return (
            base64.b64encode(buffered.getvalue()),
            MLEncodingEnum.BASE_64,
        )
