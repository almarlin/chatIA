import os
import json

# Ruta para guardar los datos de los usuarios
USER_DATA_PATH = 'data/'

# Función para cargar la memoria de un usuario
def cargar_memoria(user_id: str):
    user_file = os.path.join(USER_DATA_PATH, f'{user_id}.json')
    if os.path.exists(user_file):
        with open(user_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []  # Si no existe historial, retornamos una lista vacía

# Función para guardar la memoria de un usuario
def guardar_memoria(user_id: str, mensaje: str):
    # Cargar el historial
    memoria = cargar_memoria(user_id)
    memoria.append(mensaje)
    
    # Guardar el nuevo historial
    with open(os.path.join(USER_DATA_PATH, f'{user_id}.json'), 'w', encoding='utf-8') as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)
