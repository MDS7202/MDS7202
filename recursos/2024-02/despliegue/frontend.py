import gradio as gr
import requests
from make_prediction import make_prediction

def get_backend_prediction(
        sepal_length: float, 
        sepal_width: float, 
        petal_length: float, 
        petal_width: float,
        ):

    # payload
    data = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }

    url = "http://127.0.0.1:8000/predict" # url del back end
    response = requests.post(url, json = data) # código de respuesta
    label = response.json()["label"] # obtener contenido de la respuesta

    return label

with gr.Blocks(theme = gr.themes.Base()) as demo:
    gr.Markdown(
    """
    # Iris ML Demo
    Bienvenid@ a Iris ML demo! Esta herramienta esta diseñada para predecir la clase de una flor a partir de sus características usando Machine Learning.
    ## Cómo usar este demo?
    Usar esta herramienta es fácil! Sólo debes seguir los siguientes pasos:
    1. Fijar los valores de **Sepal Length**, **Sepal Width**, **Petal Length** y **Petal Width**.
    2. Observar el tipo de flor que predice el modelo.
    
    Eso es todo! Estás list@ para explorar y predecir diferentes tipos de flores. Que lo disfrutes!
    """)

    with gr.Row():
        with gr.Column():
            sepal_length_slider = gr.Slider(label = 'Sepal Length', minimum = 0, maximum = 10, value = 3.8)
            sepal_width_slider = gr.Slider(label = 'Sepal Width', minimum = 0, maximum = 10, value = 6.4)
            petal_length_slider = gr.Slider(label = 'Petal Length', minimum = 0, maximum = 10, value = 7.3)
            petal_width_slider = gr.Slider(label = 'Petal Width', minimum = 0, maximum = 10, value = 4.9)

        with gr.Column():
            label = gr.Text(label = 'Predicted Label') # se define un nombre para la salida
    
    with gr.Row():
        button = gr.Button(value = 'Predict!')

    # setear interactividad
    inputs = [sepal_length_slider, sepal_width_slider, petal_length_slider, petal_width_slider]
    outputs = [label]
    #button.click(fn = make_prediction, inputs = inputs, outputs = outputs) # esta linea invoca la función local
    button.click(fn = get_backend_prediction, inputs = inputs, outputs = outputs) # esta linea invoca el back end

    examples = [
        [0.5, 1.5, 2.5, 3.5], # example 1
        [1, 3, 5, 7], # example 2
    ]
    gr.Examples(examples = examples, inputs = inputs) 

    demo.launch(share = True)