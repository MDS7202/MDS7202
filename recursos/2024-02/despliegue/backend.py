from fastapi import FastAPI
from make_prediction import make_prediction

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
async def predict(# parametros de entrada
    sepal_length: float = 3.5, 
    sepal_width: float = 2.0, 
    petal_length: float = 1.6, 
    petal_width: float = 5.4,
    ) -> dict: 

    # generar prediccion
    label = make_prediction(sepal_length, sepal_width, petal_length, petal_width) 

    # retornar prediccion
    return {"label": label} 