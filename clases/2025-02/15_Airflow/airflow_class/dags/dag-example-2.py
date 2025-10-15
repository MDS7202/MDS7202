from datetime import timedelta
from airflow import DAG

from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from functions_example_2 import (
    clean_data, choose_data_branch, join_data, 
    train_lgbm, train_random_forest, choose_best_model
)

args={
    'owner' : 'MDS7202',
    'retries': 1,
}

with DAG(
    dag_id='my_second_pipeline',
    default_args=args,
    description='MLops pipeline',
    start_date = days_ago(5),
    schedule_interval='@daily',
    catchup=True) as dag:
 
    # Task 1 - Just a simple print statement
    dummy_task = EmptyOperator(task_id='Start', retries=2)  

    # Task 2 - Branch operator
    branch_task_1 = BranchPythonOperator(
        task_id='choose_data_branch',
        python_callable=choose_data_branch,
        provide_context=True,
        dag=dag
    )

    # Task 3.a
    task_download_dataset_1 = BashOperator(
        task_id='download_dataset_1',
        bash_command="curl -o " 
        "/root/airflow/data_1_{{ ds }}.csv "
        "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_1.csv"
    )

    # Task 3.b
    task_download_dataset_2 = BashOperator(
        task_id='download_dataset_2',
        bash_command="curl -o " 
        "/root/airflow/data_2_{{ ds }}.csv "
        "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_2.csv"
    )

    # Task 3.c
    task_download_dataset_3 = BashOperator(
        task_id='download_dataset_3',
        bash_command="curl -o " 
        "/root/airflow/data_3_{{ ds }}.csv "
        "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/airflow_class/data_3.csv"
    )

    # Task 4.a - Clean the data
    task_clean_data_1 = PythonOperator(
    task_id='clean_data_1',
    python_callable=clean_data,
    op_kwargs={'data_name': 'data_1'},
    trigger_rule='all_success'
    )

    # Task 4.b - Clean the data
    task_clean_data_2 = PythonOperator(
    task_id='clean_data_2',
    python_callable=clean_data,
    op_kwargs={'data_name': 'data_2'},
    trigger_rule='all_success'
    )

    # Task 4.c - Clean the data
    task_clean_data_3 = PythonOperator(
    task_id='clean_data_3',
    python_callable=clean_data,
    op_kwargs={'data_name': 'data_3'},
    trigger_rule='all_success'
    )

    # Task 5 - Join the data
    task_join_data = PythonOperator(
        task_id='join_data',
        python_callable=join_data,
        trigger_rule='one_success'
    )

    # Task 6.a - Train a ML Model using LightGBM
    task_train_lgbm_model = PythonOperator(
    task_id='ml_train_lgbm',
    python_callable=train_lgbm
    )

    # Task 6.a - Train a ML Model using LightGBM
    task_train_rf_model = PythonOperator(
    task_id='ml_train_rf',
    python_callable=train_random_forest
    )

    # Task 7 - Choose the best model
    choose_best_model_task = PythonOperator(
        task_id='choose_best_model',
        python_callable=choose_best_model,
        provide_context=True,
        trigger_rule='one_success'
    )

    # Task 8
    final_dummy_task = EmptyOperator(task_id='End', retries=1)  


    # Define the workflow process
    dummy_task >> branch_task_1
    branch_task_1 >> [task_download_dataset_1, task_download_dataset_2, task_download_dataset_3]
    task_download_dataset_1 >> task_clean_data_1
    task_download_dataset_2 >> task_clean_data_2
    task_download_dataset_3 >> task_clean_data_3
    task_clean_data_1 >> task_join_data
    task_clean_data_2 >> task_join_data
    task_clean_data_3 >> task_join_data
    task_join_data >> [task_train_lgbm_model, task_train_rf_model]
    [task_train_lgbm_model, task_train_rf_model] >> choose_best_model_task
    choose_best_model_task >> final_dummy_task
