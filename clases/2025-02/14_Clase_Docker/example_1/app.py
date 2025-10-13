import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import os
from datetime import datetime

# Crear una carpeta para almacenar las imágenes de gatos
os.makedirs("saved_cats", exist_ok=True)

def fetch_random_cat_pic():
    try:
        # Enviar una solicitud a The Cat API
        cat_api_response = requests.get("https://api.thecatapi.com/v1/images/search")
        cat_api_response.raise_for_status()
        
        # Extraer la URL de la imagen de la respuesta de la API
        cat_data = cat_api_response.json()
        cat_image_url = cat_data[0]['url']
        
        # Descargar la imagen
        image_response = requests.get(cat_image_url)
        image_response.raise_for_status()
        
        # Abrir la imagen
        cat_image = Image.open(BytesIO(image_response.content))
        
        # Generar un nombre de archivo único usando la fecha y hora actual
        image_filename = f"cat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = os.path.join("saved_cats", image_filename)
        
        # Guardar la imagen localmente
        cat_image.save(image_path)
        
        return image_path
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

iface = gr.Interface(
    fn=fetch_random_cat_pic,
    inputs=[],
    outputs=gr.Image(type="filepath", label="Random Cat Image"),
    live=True
)

iface.launch(server_name="0.0.0.0", server_port=7860)
