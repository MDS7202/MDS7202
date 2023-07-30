from fastapi import FastAPI
from joblib import load
import json
import datetime

# interfaz del servidor.
app = FastAPI()

# cargamos el modelo usando joblib
pipe = load("iris_naive_bayes.joblib")
detector_novelties = None


@app.get("/")
async def main():
    return {
        "mensaje": "Hola 🤩! Visita los docs para ver la documentación de la app.",
        "link_a_los_docs": "http://127.0.0.1:8000/docs",
    }


@app.get("/iris/")
async def predictor_iris(
    sepal_length: float,
    sepal_width: float,
    petal_length: float,
    petal_width: float,
):
    atributos = [sepal_length, sepal_width, petal_length, petal_width]

    prediccion = pipe.predict([atributos])

    return {"predicción": prediccion[0]}


# la idea es definir varias APIs en un servidor!
# en este caso, usaremos la misma iris, pero haremos un post
# esto nos permitirá usar el body en vez la url como parámetros.
@app.post("/iris/")
async def predictor_batch_iris(batch: list):
    print(batch)

    prediccion = pipe.predict(batch)
    return {"predicciones": prediccion.tolist(), "guardado": False}


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


# para ejecutar en una consola:
# curl -X 'POST' \
#   'http://127.0.0.1:8000/iris/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '[[7.2, 3.6, 6.1, 2.5],
#  [6.7, 3.0, 5.0, 1.7],
#  [4.8, 3.4, 1.9, 0.2],
#  [5.4, 3.0, 4.5, 1.5],
#  [5.6, 3.0, 4.1, 1.3],
#  [6.9, 3.1, 5.1, 2.3],
#  [5.0, 2.3, 3.3, 1.0],
#  [6.9, 3.2, 5.7, 2.3],
#  [4.7, 3.2, 1.6, 0.2],
#  [6.7, 3.1, 4.4, 1.4]]'
