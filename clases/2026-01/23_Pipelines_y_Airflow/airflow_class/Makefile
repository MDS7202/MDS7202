IMAGE_NAME = my-airflow-image
CONTAINER_NAME = my-airflow-container
PORT = 8080

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

build: ## Construye la imagen Docker
	docker build -t $(IMAGE_NAME) .

run: ## Inicia el contenedor en background (monta dags/ y logs/ como volúmenes)
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):8080 \
		-v $(PWD)/dags:/root/airflow/dags \
		-v $(PWD)/logs:/root/airflow/logs \
		$(IMAGE_NAME)

stop: ## Detiene el contenedor
	docker stop $(CONTAINER_NAME)

rm: ## Elimina el contenedor
	docker rm -f $(CONTAINER_NAME)

logs: ## Sigue los logs del contenedor en tiempo real
	docker logs -f $(CONTAINER_NAME)

restart: rm run ## Reinicia el contenedor (rm + run)

shell: ## Abre una shell bash dentro del contenedor
	docker exec -it $(CONTAINER_NAME) bash

clean: rm ## Elimina el contenedor y la imagen
	docker rmi $(IMAGE_NAME)

.PHONY: help build run stop rm logs restart shell clean
