from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Cargar el modelo GPT-2 y su tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Estructura para almacenar la memoria (historial de conversaciones)
historial_conversacion = ""

# Función para generar respuestas usando GPT-2 con memoria
def generar_respuesta(contexto: str) -> str:
    global historial_conversacion
    
    # Añadir la nueva entrada al historial
    historial_conversacion += f"Usuario: {contexto}\n"
    
    # Codificar el contexto del historial de conversación
    inputs = tokenizer.encode(historial_conversacion, return_tensors="pt")
    
    # Generar la respuesta con el modelo
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, temperature=0.2)
    
    # Decodificar y extraer la respuesta generada
    respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extraer solo la respuesta generada por el modelo (descartando el contexto)
    respuesta_usuario = respuesta[len(historial_conversacion):].strip()
    
    # Añadir la respuesta al historial
    historial_conversacion += f"Zeta: {respuesta_usuario}\n"
    
    return respuesta_usuario

# Bucle principal para la interacción
print("Escribe 'salir' para terminar la conversación.")
while True:
    entrada = input("Tú: ")
    if entrada.lower() == "salir":
        break

    respuesta = generar_respuesta(entrada)
    print("Zeta:", respuesta)
