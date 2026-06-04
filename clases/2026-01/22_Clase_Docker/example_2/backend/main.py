from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import os
import pandas as pd

class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


model = load("iris_classifier.joblib")
app = FastAPI()

data_dir = os.getenv('DATA_DIR', './data')
csv_file_path = os.path.join(data_dir, "predictions.csv")
# en caso de que no exista el directorio, lo creamos
if not os.path.exists(csv_file_path):
    df = pd.DataFrame(columns=["sepal_length", "sepal_width", "petal_length", "petal_width", "label"])
    df.to_csv(csv_file_path, index=False)

# home
@app.get("/")
def read_root():
    return {"message": "Iris Classifier API is running!"}

# predict
@app.post("/predict")
def predict(data: IrisData):
    features = [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]
    label = model.predict(features)[0]
    
    new_data = pd.DataFrame([{
        "sepal_length": data.sepal_length,
        "sepal_width": data.sepal_width,
        "petal_length": data.petal_length,
        "petal_width": data.petal_width,
        "label": label
    }])
    new_data.to_csv(csv_file_path, mode='a', header=False, index=False)
    
    return {"label": int(label)}
