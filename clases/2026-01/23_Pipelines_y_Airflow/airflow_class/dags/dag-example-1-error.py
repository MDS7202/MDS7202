"""Pipeline básico de MLOps con un error intencional (TaskFlow API).

Versión de ``dag-example-1.py`` con un error deliberado: la tarea de limpieza
intenta leer ``data1_.csv`` pero el archivo descargado se llama ``employee_attrition.csv``.
Se usa para demostrar cómo Airflow detecta, reporta y reintenta tareas fallidas.
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
    dag_id="my_first_pipeline_error",
    default_args=args,
    description="Pipeline con error intencional para demostrar el manejo de fallos",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
)
def my_first_pipeline_error():
    # Tarea 1 - Punto de inicio del proceso
    inicio = EmptyOperator(task_id="inicio")

    # Tarea 2 - Descarga del dataset (guarda como employee_attrition.csv)
    descarga = BashOperator(
        task_id="descarga_dataset",
        bash_command=(
            "curl -o /root/airflow/employee_attrition.csv "
            "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_1.csv"
        ),
    )

    # Tarea 3 - ERROR: intenta leer data1_.csv, pero el archivo real es employee_attrition.csv
    @task
    def limpiar_datos() -> None:
        _clean_data(file_path="data1_.csv")

    # Tarea 4 - No se ejecutará porque la tarea anterior fallará
    @task
    def entrenar_lgbm() -> None:
        _ml_train_LGBM()

    # Definición del flujo de trabajo
    inicio >> descarga >> limpiar_datos() >> entrenar_lgbm()


my_first_pipeline_error()
