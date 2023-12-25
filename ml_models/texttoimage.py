import torch
import base64
from diffusers import AutoPipelineForText2Image, StableDiffusionPipeline, StableDiffusionXLPipeline, \
    UNet2DConditionModel
from io import BytesIO

from models.db.mlmodel import MLModel, MLEncodingEnum


class TextToImage(MLModel):
    def __init__(self, location: str, *args, **kwargs):
        self.location = location
        # for opendallev1.1
        # self.pipeline = AutoPipelineForText2Image.from_pretrained(location, torch_dtype=torch.float16).to('cuda:0')

        # for stable diffusion
        # self.pipeline = StableDiffusionPipeline.from_pretrained(location, torch_dtype=torch.float16).to('cuda:0')

        # for dpo-sdxl-text2image-v1
        self.pipeline = StableDiffusionXLPipeline.from_pretrained(location, torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda:0")
        unet = UNet2DConditionModel.from_pretrained(f'{location}_unet', torch_dtype=torch.float16)
        self.pipeline.unet = unet
        self.pipeline.to("cuda:0")

    def execute(self, command_text: str) -> tuple[bytes, MLEncodingEnum.BASE_64]:
        image = self.pipeline(command_text, temperature=0.87).images[0]
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return (
            base64.b64encode(buffered.getvalue()),
            MLEncodingEnum.BASE_64,
        )
