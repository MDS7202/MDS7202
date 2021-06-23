# 1. Pasos iniciales

from fastapi import FastAPI

# interfaz del servidor.
app = FastAPI()


# decorador que indica el método de la llamada (get).
# este permite registrar que cualquier get que llegue a '/' sea respondido por esta función.
@app.get("/")
async def root():
    # retornamos directamente el contenido.
    # pero aquí puede haber una predicción de algún modelo,
    return {"message": "Hola a todxs!! 😄😄😄"}


# Para probar el funcionamiento de este mini-servidor:
# 0. (en el caso que no lo tengan instalado), pip install fastapi[all]
# 1. ejecutar: uvicorn main_1:app --reload
# 2. visitar en el navegador http://127.0.0.1:8000/

#  documentación: http://127.0.0.1:8000/docs#
