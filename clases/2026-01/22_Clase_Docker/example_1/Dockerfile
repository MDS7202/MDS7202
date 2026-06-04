# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt en el contenedor
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación en el contenedor
COPY . .

# Exponer el puerto que utiliza Gradio (por defecto 7860)
EXPOSE 7860

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]