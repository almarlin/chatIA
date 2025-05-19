from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
import torch
import asyncio
from threading import Thread
from memory import cargar_memoria, guardar_memoria

model_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Cargar modelo y tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# STREAMING DE RESPUESTA CON HISTORIAL
async def generate_streaming_response(user_id: str, user_message: str):
    # Cargar historial desde disco
    historial = cargar_memoria(user_id)
    
    # Construir prompt incluyendo mensaje nuevo
    historial.append(f"Usuario: {user_message}")
    prompt = ""
    for i, linea in enumerate(historial):
        if linea.startswith("Usuario:"):
            prompt += f"{linea}\n"
        elif linea.startswith("Zeta:"):
            prompt += f"{linea}\n"

    prompt += f"Usuario: {user_message}\nZeta:"

    # Codificar prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Crear streamer
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    # Parámetros de generación
    generation_kwargs = {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "max_new_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.9,
        "do_sample": True,
        "streamer": streamer,
    }

    # Lanzar la generación en un hilo
    generation_thread = Thread(target=model.generate, kwargs=generation_kwargs)
    generation_thread.start()

    respuesta = ""
    for token in streamer:
        respuesta += token
        yield token  # Streaming hacia el frontend

    # Guardar mensaje y respuesta
    guardar_memoria(user_id, f"Usuario: {user_message}")
    guardar_memoria(user_id, f"Zeta: {respuesta.strip()}")
