from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.dates import days_ago

import random

dag = DAG(
    'example_branch_dag',
    description='Ejemplo de branching en Airflow',
    schedule_interval='@daily',
    start_date=days_ago(3),
    catchup=False
)

start = DummyOperator(task_id='start', dag=dag)

def choose_branch(**kwargs):
    if random.choice([True, False]):
        return 'branch_a'
    else:
        return 'branch_b'

# Operador de branching
branch_task = BranchPythonOperator(
    task_id='branch_task',
    python_callable=choose_branch,
    provide_context=True,
    dag=dag
)

branch_a = DummyOperator(task_id='branch_a', dag=dag)
branch_b = DummyOperator(task_id='branch_b', dag=dag)

end = DummyOperator(
    task_id='end', 
    dag=dag, 
    trigger_rule='one_success'
)


start >> branch_task
branch_task >> [branch_a, branch_b]
branch_a >> end
branch_b >> end