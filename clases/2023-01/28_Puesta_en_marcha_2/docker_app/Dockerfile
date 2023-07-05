FROM python:3.10-slim-buster

# fijamos /app como la ruta en la que trabajaremos
WORKDIR /app

# copiamos desde nuestra carpeta a /app los requerimientos
COPY requirements.txt requirements.txt

# ejecutamos
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "uvicorn", "main:app", "--reload", "--host=0.0.0.0"]