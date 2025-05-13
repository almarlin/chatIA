from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch
import faiss
import os
from huggingface_hub import login

# 1. Iniciar sesión en Hugging Face (usa token solo si es necesario)
# Iniciar sesión en Hugging Face
login("")

# 2. Configurar dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 3. Cargar modelo de lenguaje
print("🔍 Cargando modelo Mistral...")
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
).to(device)

# 4. Cargar modelo de embeddings
print("🧠 Cargando modelo de embeddings...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# 5. Inicializar memoria e índice FAISS
memory = []
index = faiss.IndexFlatL2(384)  # 384 = tamaño de vector de MiniLM-L6-v2

# 6. Función para obtener contexto similar
def obtener_contexto(mensaje, k=3):
    if len(memory) == 0:
        return ""
    query_vector = embed_model.encode([mensaje], convert_to_numpy=True)
    D, I = index.search(query_vector, k)
    contexto = []
    for idx in I[0]:
        if idx < len(memory):  # Protección por si el índice está fuera de rango
            m = memory[idx]
            contexto.append(f"Usuario: {m['mensaje']}\nZeta: {m['respuesta']}")
    return "\n".join(contexto)

# 7. Función para crear el prompt
def crear_prompt(contexto, mensaje):
    return (
        "Eres Zeta, un asistente amistoso, inteligente y curioso. "
        "Recuerdas lo que te han dicho y das respuestas naturales y útiles.\n\n"
        f"Contexto previo:\n{contexto}\n\n"
        f"Usuario: {mensaje}\n"
        "Zeta:"
    )

# 8. Limpieza del texto generado
def limpiar_respuesta(texto_completo):
    partes = texto_completo.split("Zeta:")
    if len(partes) > 1:
        return partes[-1].strip()
    return texto_completo.strip()

# 9. Bucle de conversación
print("💬 Zeta está listo. Escribe 'salir' para terminar la conversación.")

while True:
    entrada = input("Tú: ").strip()
    if entrada.lower() == "salir":
        break

    contexto = obtener_contexto(entrada)
    prompt = crear_prompt(contexto, entrada)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    respuesta = limpiar_respuesta(tokenizer.decode(outputs[0], skip_special_tokens=True))

    print("Zeta:", respuesta)

    # Guardar en memoria e índice FAISS
    memory.append({"mensaje": entrada, "respuesta": respuesta})
    vector = embed_model.encode([entrada], convert_to_numpy=True)
    index.add(vector)

