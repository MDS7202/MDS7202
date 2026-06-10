"""Pipeline avanzado de MLOps con branching y selección de modelos (TaskFlow API).

Extiende el pipeline básico con tres conceptos clave:
- Bifurcación condicional (``@task.branch``) según la fecha de ejecución del DAG
  para seleccionar qué datasets descargar.
- Entrenamiento en paralelo de LightGBM y Random Forest.
- Selección automática del mejor modelo por accuracy: el valor de retorno de cada
  ``@task`` de entrenamiento fluye directamente como argumento a la tarea de selección,
  sin necesidad de XCom manual.
"""

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import dag, task
from evaluation import choose_best_model as _choose_best_model
from flow_control import choose_data_branch as _choose_data_branch
from preprocessing import clean_data as _clean_data
from preprocessing import join_data as _join_data
from training import train_lgbm as _train_lgbm
from training import train_random_forest as _train_random_forest

args = {
    "owner": "MDS7202",
    "retries": 1,
}


@dag(
    dag_id="my_second_pipeline",
    default_args=args,
    description="Pipeline avanzado de MLOps: branching, entrenamiento paralelo y selección de modelos",
    start_date=pendulum.datetime(2026, 6, 10, tz="UTC"),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
)
def my_second_pipeline():
    # Tarea 1 - Punto de inicio
    inicio = EmptyOperator(task_id="Start")

    # Tarea 2 - Bifurcación: selecciona qué datasets descargar según la fecha
    # @task.branch reemplaza a BranchPythonOperator; el retorno es la lista de task IDs a ejecutar
    @task.branch
    def elegir_rama(ds: str) -> list[str]:
        return _choose_data_branch(ds=ds)

    # Tareas 3.a/b/c - Descarga de datasets (BashOperator no tiene equivalente @task)
    descargar_1 = BashOperator(
        task_id="download_dataset_1",
        bash_command=(
            "curl -o /root/airflow/data_1_{{ ds }}.csv "
            "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_1.csv"
        ),
        do_xcom_push=False,
    )
    descargar_2 = BashOperator(
        task_id="download_dataset_2",
        bash_command=(
            "curl -o /root/airflow/data_2_{{ ds }}.csv "
            "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_2.csv"
        ),
        do_xcom_push=False,
    )
    descargar_3 = BashOperator(
        task_id="download_dataset_3",
        bash_command=(
            "curl -o /root/airflow/data_3_{{ ds }}.csv "
            "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_3.csv"
        ),
        do_xcom_push=False,
    )

    # Tareas 4.a/b/c - Limpieza individual de cada dataset
    # trigger_rule="all_success" porque cada tarea solo depende de su propia descarga
    @task(trigger_rule="all_success")
    def limpiar_1(ds: str) -> None:
        _clean_data(file_path=f"data_1_{ds}.csv", data_key=f"data_1_{ds}")

    @task(trigger_rule="all_success")
    def limpiar_2(ds: str) -> None:
        _clean_data(file_path=f"data_2_{ds}.csv", data_key=f"data_2_{ds}")

    @task(trigger_rule="all_success")
    def limpiar_3(ds: str) -> None:
        _clean_data(file_path=f"data_3_{ds}.csv", data_key=f"data_3_{ds}")

    # Tarea 5 - Combinación de los datasets limpios
    # trigger_rule="one_success": ejecuta cuando al menos uno de los datasets está limpio
    @task(trigger_rule="one_success")
    def unir_datos(ds: str) -> None:
        _join_data(ds=ds)

    # Tareas 6.a/b - Entrenamiento paralelo; el dict de retorno fluye automáticamente
    # como argumento a seleccionar_mejor (sin ti.xcom_push ni ti.xcom_pull)
    @task
    def entrenar_lgbm(ds: str) -> dict:
        return _train_lgbm(ds=ds)

    @task
    def entrenar_rf(ds: str) -> dict:
        return _train_random_forest(ds=ds)

    # Tarea 7 - Selección del mejor modelo
    # trigger_rule="one_success": funciona aunque uno de los entrenamientos falle
    @task(trigger_rule="one_success")
    def seleccionar_mejor(lgbm_result: dict, rf_result: dict) -> None:
        _choose_best_model(lgbm_result=lgbm_result, rf_result=rf_result)

    # Tarea 8 - Fin del proceso
    fin = EmptyOperator(task_id="End")

    # Definición del flujo de trabajo
    rama = elegir_rama(ds="{{ ds }}")
    inicio >> rama >> [descargar_1, descargar_2, descargar_3]

    clean_1 = limpiar_1(ds="{{ ds }}")
    clean_2 = limpiar_2(ds="{{ ds }}")
    clean_3 = limpiar_3(ds="{{ ds }}")
    descargar_1 >> clean_1
    descargar_2 >> clean_2
    descargar_3 >> clean_3

    union = unir_datos(ds="{{ ds }}")
    [clean_1, clean_2, clean_3] >> union

    lgbm = entrenar_lgbm(ds="{{ ds }}")
    rf = entrenar_rf(ds="{{ ds }}")
    union >> [lgbm, rf]

    mejor = seleccionar_mejor(lgbm_result=lgbm, rf_result=rf)
    mejor >> fin


my_second_pipeline()
