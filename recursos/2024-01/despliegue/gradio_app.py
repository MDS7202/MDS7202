import gradio as gr
from make_prediction import make_prediction

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
            sepal_length_slider = gr.Slider(label = 'Sepal Length', minimum = 0, maximum = 10)
            sepal_width_slider = gr.Slider(label = 'Sepal Width', minimum = 0, maximum = 10)
            petal_length_slider = gr.Slider(label = 'Petal Length', minimum = 0, maximum = 10)
            petal_width_slider = gr.Slider(label = 'Petal Width', minimum = 0, maximum = 10)

        with gr.Column():
            label = gr.Text(label = 'Predicted Label') # se define un nombre para la salida
    
    with gr.Row():
        button = gr.Button(value = 'Predict!')

    # setear interactividad
    inputs = [sepal_length_slider, sepal_width_slider, petal_length_slider, petal_width_slider]
    outputs = [label]
    button.click(fn = make_prediction, inputs = inputs, outputs = outputs)

    examples = [
        [0.5, 1.5, 2.5, 3.5], # example 1
        [1, 3, 5, 7], # example 2
    ]
    gr.Examples(examples = examples, inputs = inputs) 

    demo.launch(debug = False)