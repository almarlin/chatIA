from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from mistral_chatbot import generate_streaming_response
from pydantic import BaseModel
# from chatbot import generar_respuesta
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

@app.get("/chat/stream")
async def chat_stream(user_id: str, message: str):
    async def event_generator():
        historial = cargar_memoria(user_id)

        # Guardar mensaje del usuario
        guardar_memoria(user_id, f"Usuario: {message}")

        response_text = ""
        async for token in generate_streaming_response(message, historial):
            response_text += token
            yield f"data: {token}\n\n"

        # Guardar la respuesta completa del asistente
        guardar_memoria(user_id, f"Zeta: {response_text.strip()}")
        yield f"data: [END]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")



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
