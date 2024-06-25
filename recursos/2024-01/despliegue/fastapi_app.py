from fastapi import FastAPI
from make_prediction import make_prediction
import uvicorn

# init app
app = FastAPI()

# def home
@app.get('/') # ruta
async def home():
    return {'Hello': 'World'}

@app.get('/classroom') # ruta
def classroom():
    return {'Message': 'This is my first API :)'}

# def predict method
@app.post("/predict") # ruta
async def predict(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float): # parametros de entrada

    label = make_prediction(sepal_length, sepal_width, petal_length, petal_width) # generar prediccion

    return {"label": label} # retornar prediccion

if __name__ == '__main__':
    uvicorn.run('fastapi_app:app', port = 8000)