from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from sentence_transformers import SentenceTransformer, util
import torch
import json

# 🔐 Autenticación si es privada (sólo si el modelo lo requiere)
# from huggingface_hub import login
# login(token="TU_TOKEN")

# 📌 Configuración
MODEL_NAME = "openchat/openchat-3.5-0106"
MEMORY_FILE = "memory.json"

# 💻 Carga el modelo en 4-bit y en GPU
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    load_in_4bit=True
)

# 🚀 Crea el pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)

# 🧠 Carga modelo de embeddings para memoria
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 🗂️ Funciones de memoria
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def add_memory(memory, text):
    embedding = embedder.encode(text).tolist()
    memory.append({"text": text, "embedding": embedding})
    save_memory(memory)

def retrieve_relevant(memory, query, top_k=3):
    if not memory:
        return []
    query_emb = embedder.encode(query)
    embeddings = [m["embedding"] for m in memory]
    scores = util.cos_sim(query_emb, embeddings)[0]
    top_results = sorted(zip(scores, memory), key=lambda x: x[0], reverse=True)[:top_k]
    return [r[1]["text"] for r in top_results]

# 🧠 Memoria activa
memory = load_memory()

print("🟢 Zeta (OpenChat 3.5 en 4-bit) está listo. Escribe 'salir' para terminar.")

# 💬 Loop de conversación
while True:
    entrada = input("Tú: ").strip()
    if entrada.lower() == "salir":
        print("Zeta: ¡Hasta luego!")
        break

    relevantes = retrieve_relevant(memory, entrada)
    contexto = "\n".join(relevantes)
    prompt = f"Eres Zeta, un asistente amable y creativo.\nContexto:\n{contexto}\nUsuario: {entrada}\nZeta:"

    respuesta = pipe(prompt, max_new_tokens=100, temperature=0.7, top_p=0.9, do_sample=True)[0]["generated_text"]
    # Extraer solo lo nuevo
    output = respuesta[len(prompt):].strip().split("\n")[0]

    print("Zeta:", output)

    # Guardar en memoria
    add_memory(memory, f"Usuario dijo: {entrada}")
    add_memory(memory, f"Zeta respondió: {output}")
