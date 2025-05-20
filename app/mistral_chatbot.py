from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    StoppingCriteria,
    StoppingCriteriaList,
)
import torch
import asyncio
from functools import partial

model_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Cargar tokenizer y modelo
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

# Detener si el modelo intenta hablar como el usuario
class StopOnDialogueTag(StoppingCriteria):
    def __init__(self, tokenizer, stop_strings=["Usuario:", "User:", "Human:", "usuario:","user:"]):
        self.tokenizer = tokenizer
        self.stop_ids = [tokenizer.encode(s, add_special_tokens=False) for s in stop_strings]

    def __call__(self, input_ids, scores, **kwargs):
        for stop_seq in self.stop_ids:
            if len(input_ids[0]) >= len(stop_seq):
                if input_ids[0].tolist()[-len(stop_seq):] == stop_seq:
                    return True
        return False


# Construcción del prompt
def construir_prompt(historial, mensaje_usuario):
    prompt = (
        "Instrucciones: Tú eres Zeta, un asistente informático. Responde a las preguntas del usuario de forma útil y profesional. "
        "Nunca generes texto que empiece por 'Usuario:', 'Alvaro:', 'Human:' u otras marcas de usuario. "
        "Solo responde como Zeta.\n\n"
    )
    for entrada in historial:
        if entrada.startswith("Zeta:"):
            prompt += entrada.strip() + "\n"
    prompt += f"{mensaje_usuario}\nZeta:"
    return prompt

# Generación streaming
async def generate_streaming_response(mensaje_usuario, historial):
    prompt = construir_prompt(historial, mensaje_usuario)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    generation_kwargs = {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "max_new_tokens": 60,
        "temperature": 0.7,
        "do_sample": True,
        "streamer": streamer,
        "stopping_criteria": StoppingCriteriaList([StopOnDialogueTag(tokenizer)])
    }

    loop = asyncio.get_event_loop()
    task = loop.run_in_executor(None, partial(model.generate, **generation_kwargs))

    async for token in wrap_stream(streamer):
        yield token

    await task

# Streaming wrapper
async def wrap_stream(streamer):
    for token in streamer:
        yield token
        await asyncio.sleep(0)
