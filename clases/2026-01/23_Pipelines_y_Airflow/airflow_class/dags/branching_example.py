"""Ejemplo mínimo de branching en Airflow con TaskFlow API.

Muestra cómo usar ``@task.branch`` para dividir el flujo de ejecución
en dos ramas alternativas de forma aleatoria.
"""
import random

import pendulum
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator


@dag(
    dag_id="example_branch_dag",
    description="Ejemplo de branching con @task.branch",
    schedule="@daily",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
)
def example_branch_dag():
    inicio = EmptyOperator(task_id="start")
    fin = EmptyOperator(task_id="end", trigger_rule="one_success")

    # @task.branch reemplaza a BranchPythonOperator
    # El valor de retorno debe ser un task_id (str) o lista de task_ids
    @task.branch
    def elegir_rama() -> str:
        """Elige aleatoriamente entre ``branch_a`` y ``branch_b``.

        Returns:
            Task ID de la rama a ejecutar.
        """
        return random.choice(["branch_a", "branch_b"])

    rama_a = EmptyOperator(task_id="branch_a")
    rama_b = EmptyOperator(task_id="branch_b")

    inicio >> elegir_rama() >> [rama_a, rama_b]
    [rama_a, rama_b] >> fin


example_branch_dag()
