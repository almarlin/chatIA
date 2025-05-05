from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import generar_respuesta
from memory import cargar_memoria, guardar_memoria
import uvicorn
from pathlib import Path
import json



app = FastAPI()

DATA_DIR = Path("data/users")
DATA_DIR.mkdir(parents=True, exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar a ["http://localhost:3000"] en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos simulada
with open(USERS_FILE, "r",encoding="utf-8") as f:
    users_db = json.load(f)

# Modelos de datos
class ChatRequest(BaseModel):
    user_id: str
    message: str

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Estructura de la petición para el chat
class Chat(BaseModel):
    user_id: str
    message: str

# Cargar usuarios existentes (si el archivo existe)
def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Guardar usuarios
def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

# Endpoints
# Cargar el modelo de transformers (DialoGPT, GPT-2, etc.)
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")
@app.post("/chat")
async def chat_endpoint(chat: Chat):
    # Cargar el historial de conversación del usuario
    textos_previos = cargar_memoria(chat.user_id)
    
    # Crear el contexto que el chatbot utilizará (historial + mensaje actual)
    contexto = " ".join(textos_previos) + " " + chat.message
    
    # Generar una respuesta con el modelo GPT-2
    respuesta = generar_respuesta(contexto)
    
    # Guardar el mensaje actual en la memoria del usuario
    guardar_memoria(chat.user_id, chat.message)
    
    # Devolver la respuesta generada
    return {"respuesta": respuesta}

# Registro
@app.post("/register")
async def register(user: UserRegister):
    users = load_users()

    if user.username in users:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    users[user.username] = {"password": user.password}
    save_users(users)

    # Crear archivo de conversación vacío
    with open(DATA_DIR / f"{user.username}.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    return {"mensaje": f"Usuario '{user.username}' registrado correctamente"}

@app.post("/login")
async def login(user: UserLogin):
    with open(USERS_FILE, "r",encoding="utf-8") as f:
        users_db = json.load(f)
    if user.username not in users_db or users_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"mensaje": f"Sesión iniciada como '{user.username}'"}

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    with open(USERS_FILE, "r",encoding="utf-8") as f:
        users_db = json.load(f)
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"username": user_id}

# Ejecutar el servidor
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
