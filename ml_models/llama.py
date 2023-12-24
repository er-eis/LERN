import torch
from transformers import AutoTokenizer, LlamaForCausalLM

from models.db.mlmodel import MLModel, MLEncodingEnum


class LLAMA(MLModel):
    def __init__(self, location: str, *args, **kwargs):
        self.location = location
        self.tokenizer = AutoTokenizer.from_pretrained(location)
        self.model = LlamaForCausalLM.from_pretrained(location, device_map="cuda:0", torch_dtype=torch.float16)

    def execute(self, command_text: str) -> tuple[bytes, MLEncodingEnum.UTF_8]:
        model_inputs = self.tokenizer([command_text], return_tensors="pt").to("cuda:0")
        generated_ids = self.model.to("cuda:0").generate(**model_inputs, max_new_tokens=1500, temperature=0.91, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1)
        command_text = " ".join(
            self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        ).replace("\n", " ")

        return (
            command_text.encode(MLEncodingEnum.UTF_8.value),
            MLEncodingEnum.UTF_8,
        )
