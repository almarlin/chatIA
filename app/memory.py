import os
import json

DATA_PATH = "app/data/usuarios"

def ruta_usuario(user_id: str) -> str:
    return os.path.join(DATA_PATH, f"{user_id}.json")

def cargar_memoria(user_id: str):
    ruta = ruta_usuario(user_id)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_memoria(user_id: str, mensaje: str):
    mensajes = cargar_memoria(user_id)
    mensajes.append(mensaje)
    with open(ruta_usuario(user_id), "w", encoding="utf-8") as f:
        json.dump(mensajes, f, ensure_ascii=False, indent=2)
