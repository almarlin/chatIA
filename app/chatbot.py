from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.memory import cargar_memoria, guardar_memoria

modelo = SentenceTransformer('all-MiniLM-L6-v2')  # modelo gratuito y ligero

index = faiss.IndexFlatL2(384)
usuarios_textos = {}

def responder(user_id: str, mensaje: str) -> str:
    # Cargar historial del usuario
    textos_previos = cargar_memoria(user_id)
    usuarios_textos[user_id] = textos_previos

    # Crear embedding del mensaje actual
    embedding = modelo.encode([mensaje])[0]

    # Agregarlo al índice de búsqueda (memoria en RAM)
    if len(textos_previos) > 0:
        embeddings_anteriores = modelo.encode(textos_previos)
        index.add(np.array(embeddings_anteriores))

        # Buscar el mensaje más cercano
        D, I = index.search(np.array([embedding]), k=1)
        contexto = textos_previos[I[0][0]]
    else:
        contexto = "Primera vez que hablas conmigo."

    # Generar respuesta simple
    respuesta = f"Recuerdo que dijiste: '{contexto}'. ¿Quieres contarme más?"

    # Guardar mensaje actual en historial
    guardar_memoria(user_id, mensaje)

    return respuesta
