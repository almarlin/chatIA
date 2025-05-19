# from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
# import torch
# from threading import Thread

# MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

# # Tokenizador y modelo
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     device_map="auto",
#     torch_dtype=torch.float16,
# )

# # Historial por usuario
# historiales = {}

# def generar_respuesta(user_id: str, contexto: str) -> str:
#     if user_id not in historiales:
#         historiales[user_id] = []

#     historiales[user_id].append(f"Usuario: {contexto}")
#     prompt = "\n".join(historiales[user_id]) + "\nAsistente:"

#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

#     generation_kwargs = {
#         "input_ids": inputs["input_ids"],
#         "attention_mask": inputs["attention_mask"],
#         "max_new_tokens": 60,
#         "temperature": 0.7,
#         "top_p": 0.9,
#         "do_sample": True,
#         "streamer": streamer,
#     }

#     thread = Thread(target=model.generate, kwargs=generation_kwargs)
#     thread.start()

#     respuesta = ""
#     for new_text in streamer:
#         respuesta += new_text

#     historiales[user_id].append(f"Asistente: {respuesta.strip()}")
#     return respuesta.strip()
