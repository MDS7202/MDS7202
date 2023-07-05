# APP Predicción de Iris

- Para hacer un build de la imagen: 

```bash
$ cd clases/2023-01/28_Puesta_en_marcha_2/docker_app
# --tag <arg> indica que la imagen tendrá un tag asociado
$ docker build --tag predictor-iris .
```

- Para ver las imágenes creadas:

```bash
$ docker images
```

- Para crear un contenedor (ejecutar la imagen recién creada):

````bash
# -d indica en modo background, es decir, no veremos las salidas de la terminal.
# -p <port_1:port_2> indica que el puerto de la imagen será expuesto al puerto del host.
$ docker run -d -p 8000:8000 predictor-iris
```

- Para ver las imágenes corriendo

```bash
$ docker ps
```

- Para detener la imagen

````bash
# --publish , -p <port_1:port_2> indica que el puerto de la imagen será expuesto al puerto del host.
docker rm -f <nombre de la imagen (ver ps)>
```

- Para ejecutar la imagen de forma interactiva (ver los logs del terminal)

````bash
# --publish , -p <port_1:port_2> indica que el puerto de la imagen será expuesto al puerto del host
$ docker run -p 8000:8000 predictor-iris
```

- Ver el cheatsheet para el resto de operaciones.