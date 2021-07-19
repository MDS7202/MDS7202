# APP Predicción de Iris

Para hacer un build de la imagen: 

```bash
cd ./MDS7202/clases/25_contenedores/app_2
# --tag <arg> indica que la imagen tendrá un tag asociado
docker build --tag predictor-iris .
```

Para ejecutar la imagen recién creada:

````bash
# --publish , -p <port_1:port_2> indica que el puerto de la imagen será expuesto al puerto del host
docker run -d -p 8000:8000 predictor-iris
```

Para ejecutar la app completamente (incluida la base de datos):

````bash
docker-compose -f docker-compose.dev.yml up --build
```