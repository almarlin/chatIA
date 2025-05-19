from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from sentence_transformers import SentenceTransformer, util
import torch, json
from huggingface_hub import login

# 🔐 Autenticación si es privada (sólo si el modelo lo requiere)

login(token="")


# 📌 Configuración
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
MEMORY_FILE = "memory.json"

# 🧠 Tokenizer y modelo en GPU
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16
)

# 🌀 Streamer para mostrar token por token
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

# 🔎 Embeddings para memoria
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 📁 Funciones de memoria
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

# 🧠 Carga memoria
memory = load_memory()

print("🟢 Zeta (Mistral 7B con streaming) está lista. Escribe 'salir' para terminar.")

# 💬 Bucle de conversación
while True:
    entrada = input("Tú: ").strip()
    if entrada.lower() == "salir":
        print("Zeta: ¡Hasta luego!")
        break

    relevantes = retrieve_relevant(memory, entrada)
    contexto = "\n".join(relevantes)
    
    # ⚙️ Prompt para Mistral (instrucciones entre etiquetas [INST])
    prompt = f"<s>[INST] Eres Zeta, un asistente amable y creativo.\nContexto:\n{contexto}\nUsuario: {entrada} [/INST]"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    print("Zeta: ", end="", flush=True)
    model.generate(
        **inputs,
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True,
        streamer=streamer
    )

    # Guarda en memoria (si quieres capturar la respuesta exacta, podemos hacerlo sin el streamer)
    add_memory(memory, f"Usuario dijo: {entrada}")
    # También podrías capturar la salida con `StoppingCriteria` o usar `tokenizer.decode` si se desea
