import pickle

# load model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

labels_dict = {0: 'setosa', 1: 'versicolor', 2: 'virginica'} # label dict
def make_prediction(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
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