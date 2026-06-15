"""Pipeline básico de MLOps con Airflow (TaskFlow API).

Descarga un dataset de empleados, lo limpia y entrena un modelo LightGBM.
Sirve como introducción a los conceptos de DAG, operadores básicos y la TaskFlow API.

Diferencias respecto a la API clásica:
- ``@dag`` reemplaza al bloque ``with DAG(...)``.
- ``@task`` reemplaza a ``PythonOperator``; no hay que especificar ``python_callable``.
- El valor de retorno de cada ``@task`` se propaga automáticamente al XCom.
"""

import pendulum
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from preprocessing import clean_data as _clean_data
from training import ml_train_LGBM as _ml_train_LGBM

args = {
    "owner": "MDS7202",
    "retries": 1,
}


@dag(
    dag_id="my_first_pipeline",
    default_args=args,
    description="Pipeline básico de MLOps: descarga, limpieza y entrenamiento",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="47 17 * * *",
)
def my_first_pipeline():
    # Tarea 1 - Punto de inicio del proceso
    inicio = EmptyOperator(task_id="inicio")

    # Tarea 2 - Descarga del dataset (BashOperator: no tiene equivalente @task)
    descarga = BashOperator(
        task_id="descarga_dataset",
        bash_command=(
            "curl -o /root/airflow/employee_attrition.csv "
            "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_1.csv"
        ),
    )

    # Tarea 3 - Limpieza y codificación de los datos
    @task
    def limpiar_datos() -> None:
        _clean_data(file_path="employee_attrition.csv")

    # Tarea 4 - Entrenamiento del modelo LightGBM
    @task
    def entrenar_lgbm() -> None:
        _ml_train_LGBM()

    # Definición del flujo de trabajo
    inicio >> descarga >> limpiar_datos() >> entrenar_lgbm()


my_first_pipeline()
