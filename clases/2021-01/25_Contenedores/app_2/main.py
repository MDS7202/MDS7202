from fastapi import FastAPI
from joblib import load
import mysql.connector
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
    sepal_length: float, sepal_width: float, petal_length: float, petal_width: float,
):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    atributos = [sepal_length, sepal_width, petal_length, petal_width]

    prediccion = pipe.predict([atributos])

    # insertar

    try:
        mydb = mysql.connector.connect(
            host="mysqldb", user="root", password="p@ssw0rd1", database="registros"
        )
        cursor = mydb.cursor()

        insert = (
            "INSERT INTO registro "
            "(time, sepal_length, sepal_width, petal_length, petal_width, prediction) "
            f"VALUES ('{timestamp}', {sepal_length}, {sepal_width}, {petal_length}, {petal_width}, '{str(prediccion[0])}')"
        )
        print(insert)

        cursor.execute(insert)
        mydb.commit()

    except Exception as e:
        print(e)

    return {"predicción": prediccion[0], "guardado": True}


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


@app.post("/registros/")
async def get_registros():
    mydb = mysql.connector.connect(
        host="mysqldb", user="root", password="p@ssw0rd1", database="registros"
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM registro")

    row_headers = [x[0] for x in cursor.description]  # this will extract row headers

    results = cursor.fetchall()
    print(results)
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    print(json_data)

    return json.dumps(json_data, default=default, ensure_ascii=False)


@app.get("/initdb")
def db_init():
    mydb = mysql.connector.connect(host="mysqldb", user="root", password="p@ssw0rd1")
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS registros")
    cursor.execute("CREATE DATABASE registros")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb", user="root", password="p@ssw0rd1", database="registros"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS registro")
    cursor.execute(
        "CREATE TABLE registro ("
        "time DATETIME,"
        "sepal_length FLOAT,"
        "sepal_width FLOAT,"
        "petal_length FLOAT,"
        "petal_width FLOAT,"
        "prediction TINYTEXT"
        ")"
    )
    cursor.close()

    return {"status": "init database"}


# para probar la api:
# 1. ejecutar: uvicorn main_4:app --reload
# 2. ir a la documentación para ejecutar una llamada a la api: http://127.0.0.1:8000/docs#

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
