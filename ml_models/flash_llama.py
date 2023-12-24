import random

from transformers import AutoTokenizer, LlamaForCausalLM

from models.db.mlmodel import MLModel, MLEncodingEnum


# todo: this likely generalizes beyond flash llama
class FlashLLAMA(MLModel):
    def __init__(self, location: str, *args, **kwargs):
        self.location = location
        self.tokenizer = AutoTokenizer.from_pretrained(location)
        self.model = LlamaForCausalLM.from_pretrained(location)

    def execute(self, command_text: str) -> tuple[bytes, MLEncodingEnum.UTF_8]:
        for _ in range(random.randint(5, 30)):
            model_inputs = self.tokenizer([command_text], return_tensors="pt").to("cpu")
            generated_ids = self.model.generate(**model_inputs)
            command_text = " ".join(
                self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
            ).replace("\n", " ")

        return (
            command_text.encode(MLEncodingEnum.UTF_8.value),
            MLEncodingEnum.UTF_8,
        )
