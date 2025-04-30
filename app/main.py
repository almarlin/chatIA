from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.chatbot import responder

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    respuesta = responder(chat.user_id, chat.message)
    return {"respuesta": respuesta}
