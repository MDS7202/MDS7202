from fastapi import FastAPI
from joblib import load

# interfaz del servidor.
app = FastAPI()

# cargamos el modelo usando joblib
# noten que para cargar un modelo es necesario tener instalada
# la misma versión de la librería que están ocupando (scikit-learn en este caso)
gnb = load("iris_naive_bayes.joblib")


@app.get("/iris/")
async def predictor_iris(
    sepal_length: float, sepal_width: float, petal_length: float, petal_width: float,
):

    atributos = [[sepal_length, sepal_width, petal_length, petal_width]]

    prediccion = gnb.predict(atributos)
    return {"predicción": prediccion[0]}


# para probar la api:
# 1. ejecutar: uvicorn main_3:app --reload
# 2. http://127.0.0.1:8000/iris/?sepal_length=6.3&sepal_width=2.8&petal_length=5.1&petal_width=1.5

#  documentación: http://127.0.0.1:8000/docs#
