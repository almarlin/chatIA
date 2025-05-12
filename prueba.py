from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch
import faiss
import json
import os
from huggingface_hub import login

# Iniciar sesión en Hugging Face
login("")




# Cargar el modelo de lenguaje
print("Cargando modelo...")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.1",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Verifica si tienes una GPU disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Cargar modelo de embeddings
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Simular memoria cargada (sin usar archivo externo)
memory = []

# Construir corpus y el índice FAISS si hay memoria
corpus = [item["usuario"] + ": " + item["mensaje"] for item in memory]
if len(corpus) > 0:
    corpus_vectors = embed_model.encode(corpus, convert_to_numpy=True)
    index = faiss.IndexFlatL2(corpus_vectors.shape[1])
    index.add(corpus_vectors)
else:
    index = None

# Función para obtener contexto similar
def obtener_contexto(mensaje, k=3):
    if not index:
        return ""
    query_vector = embed_model.encode([mensaje])[0].reshape(1, -1)
    D, I = index.search(query_vector, k)
    similares = []
    for i in I[0]:
        entrada = memory[i]
        similares.append(f"Usuario: {entrada['mensaje']}\nZeta: {entrada['respuesta']}")
    return "\n".join(similares)


# Prompt base con personalidad
def crear_prompt(contexto, mensaje):
    return f"""Eres Zeta, un asistente amistoso, inteligente y curioso. Recuerdas cosas que te han dicho antes y respondes de manera natural.
Contexto previo relevante:
{contexto}

Usuario: {mensaje}
Zeta:"""

# Bucle de conversación
print("🧠 Escribe 'salir' para terminar la conversación.")
while True:
    entrada = input("Tú: ")
    if entrada.lower() == "salir":
        break

    contexto = obtener_contexto(entrada)
    prompt = crear_prompt(contexto, entrada)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=100, pad_token_id=tokenizer.eos_token_id)
    respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True).split("Zeta:")[-1].strip()

    print("Zeta:", respuesta)

    # Guardar en memoria
    nuevo = {"usuario": "usuario", "mensaje": entrada, "respuesta": respuesta}
    memory.append(nuevo)

    # Actualizar índice FAISS
    corpus.append(nuevo["usuario"] + ": " + nuevo["mensaje"])
    vector = embed_model.encode([corpus[-1]], convert_to_numpy=True)
    if index is None:
        index = faiss.IndexFlatL2(vector.shape[1])
    index.add(vector)
