from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Cargar el modelo GPT-2 y su tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Función para generar respuestas utilizando GPT-2
def generar_respuesta(contexto: str) -> str:
    # Codificar el contexto del usuario (historial de mensajes)
    inputs = tokenizer.encode(contexto, return_tensors="pt")
    
    # Generar la respuesta con el modelo
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2,temperature=0.2)
    
    # Decodificar y devolver la respuesta generada
    respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return respuesta
