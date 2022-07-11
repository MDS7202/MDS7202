# 2. Parámetros.

from typing import Optional

from fastapi import FastAPI

# interfaz del servidor.
app = FastAPI()

personas = [
    {"nombre": "Ignacio Meza", "equipo_docente": True, "alumno": False},
    {"nombre": "Maria Perez", "equipo_docente": False, "alumno": True},
    {"nombre": "Juanito Perez", "equipo_docente": False, "alumno": True},
]

# en este decorador indicamos que se registre una api que de tipo get
# sobre la ruta /pesonas y con un parámetro id.
# noten que estos no son queries, si no que rutas. Las queries se hacen usando ?id=algo
@app.get("/personas/{id}")
async def obtener_persona(id: int):
    # nota: agregar un tipo a id hará que se transforme de forma automática a este.
    if id >= len(personas):
        return {"msg": "Error!!!, esa persona no está registrada en la bbdd"}

    return personas[id]


# Para probar el funcionamiento de este mini-servidor:
# 1. ejecutar: uvicorn main_2:app --reload
# 2. visitar en el navegador http://127.0.0.1:8000/personas/0

#  documentación: http://127.0.0.1:8000/docs#
