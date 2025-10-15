from datetime import timedelta
from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from functions_example_1 import clean_data, ml_train_LGBM

args={
    'owner' : 'MDS7202',
    'retries': 1,
}

with DAG(
    dag_id='my_first_pipeline', ## Name of DAG run
    default_args=args,
    description='MLops pipeline',
    start_date = days_ago(1),
    schedule = None) as dag:
 
    # Task 1 - Just a simple print statement
    dummy_task = EmptyOperator(task_id='Starting_the_process', retries=2)  

    # Task 2 - Download the dataset with BashOperator
    task_download_dataset = BashOperator(
        task_id='download_dataset',
        bash_command="curl -o " 
        "/root/airflow/employee_attrition.csv "
        "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_1.csv"
    )

    # Task 3 - Clean the data
    task_clean_data = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data
    )

    # Task 4 - Train a ML Model using LightGBM
    task_train_lgbm_model = PythonOperator(
    task_id='ml_train_lgbm',
    python_callable=ml_train_LGBM
    )

    # Define the workflow process
    dummy_task >> task_download_dataset >> task_clean_data >> task_train_lgbm_model