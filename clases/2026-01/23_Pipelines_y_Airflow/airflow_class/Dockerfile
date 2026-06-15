# Utiliza una imagen base con Python instalado
FROM python:3.13-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /root/airflow

# Establece la variable de entorno AIRFLOW_HOME
ENV AIRFLOW_HOME=/root/airflow
ENV AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_PASSWORDS_FILE=/root/airflow/passwords.json
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_POOL_SIZE=10
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_MAX_OVERFLOW=20
ENV AIRFLOW__CORE__PARALLELISM=8
ENV AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG=4

# Instalar dependencias del sistema y uv
RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv

# Instala Apache Airflow y dependencias en una sola capa
RUN uv pip install --system \
    apache-airflow \
    scikit-learn \
    pandas \
    numpy \
    lightgbm \
    joblib

# Crea directorios y archivo de credenciales con contraseña fija
RUN mkdir -p $AIRFLOW_HOME/logs \
    && echo '{"admin": "admin"}' > $AIRFLOW_HOME/passwords.json

# Expone el puerto 8080 para el servidor web de Airflow
EXPOSE 8080

# Copia las carpetas necesarias al contenedor
COPY ./dags $AIRFLOW_HOME/dags
COPY ./plugins $AIRFLOW_HOME/plugins

# standalone hace db migrate + crea usuario admin + inicia scheduler y api-server
CMD ["airflow", "standalone"]
