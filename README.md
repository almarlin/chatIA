# Zeta AI

## Requisitos

Para poder iniciar el proyecto es necesario cumplir los siguientes requisitos:
- Node
- Nvidia rapids
- Token de hugginface

Node se utiliza para el frontend, realizado con React.js

Nvidia rapids es necesario para que el modelo funcione correctamente y más veloz.

Es necesario el token de hugginface ya que el modelo utilizado para el chatbot es de acceso a través de token. Será necesario crear una cuenta, crear un token y solicitar acceso en: **https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2**

Una vez solicitado el acceso se debe iniciar sesión desde la consola con: 
```
pip install huggingface_hub
huggingface-cli login
```
A continuación pega el token y ya habrás iniciado sesión.

## Despliegue
Se necesitan 2 consolas en la ruta del proyecto, una apuntando a `/frontend` y otra a `/app`. Ambas consolas deben ser de **ubuntu** o **wsl** y tener activo **nvidia-rapids**. Normalmente con un comando parecido a `conda activate rapids-XX.XX`.

1. Frontend
En la consola `/frontend` realizar `npm install` y posteriormente `npm start`.

2. App
En la consola `/app` realizar `python main.py`.

Una vez hayan cargado todos los servicios, ya estará lista la aplicación.


### Autor
**Programación de Inteligencia Artificial
CE en Inteligencia Artificial y Big Data
Álvaro Martínez Lineros**


