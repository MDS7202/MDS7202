import numpy as np

labels_dict = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}

def make_prediction(model, sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    '''
    función que devuelve la predicción del modelo dado un set de atributos
    '''

    # mantener el orden!
    features = [
        [sepal_length, sepal_width, petal_length, petal_width] # obs to predict
    ]
    
    prediction = model.predict(features).item() # make prediction
    label = labels_dict[prediction] # transform to label

    return label # return prediction