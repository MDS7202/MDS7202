from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from airflow.models import Variable
from sklearn.metrics import accuracy_score
import pendulum
import joblib
import os
import pandas as pd

def choose_data_branch(ds, **kwargs):
    threshold_date = '2024-06-28'
    ti = kwargs['ti']
    if ds < threshold_date:
        ti.xcom_push(key='data_selected', value=[f"data_1_{ds}", f"data_2_{ds}"])
        return ['download_dataset_1', 'download_dataset_2']
    else:
        ti.xcom_push(key='data_selected', value=[f"data_1_{ds}", f"data_3_{ds}"])
        return ['download_dataset_1', 'download_dataset_3']
    

def clean_data(data_name, ds, **kwargs):
    df = pd.read_csv(f"{data_name}_{ds}.csv", on_bad_lines='skip')
    df = df.drop(columns=['Employee ID'])
    X = df.drop(columns=['Attrition'])
    y = df['Attrition']
    categorical_columns = X.select_dtypes(include=['object']).columns
    df_transformed = pd.get_dummies(X, columns=categorical_columns, drop_first=True)
    df_transformed = pd.concat([df_transformed, y], axis=1)
    df_transformed.to_csv("clean_employee_attrition.csv")
    Variable.set(f"{data_name}_{ds}", df_transformed.to_json())


def join_data(**kwargs):
    ti = kwargs['ti']
    variable_keys = ti.xcom_pull(key='data_selected', task_ids='choose_data_branch')
    data_list = []
    for key in variable_keys:
        data = pd.read_json(Variable.get(key))
        data_list.append(data)
    df = pd.concat(data_list, axis=0)
    df.to_csv("clean_employee_attrition.csv")


def train_lgbm(ds, **kwargs):
    ti = kwargs['ti']
    # Load the cleaned data
    df = pd.read_csv("clean_employee_attrition.csv", index_col=0, on_bad_lines='skip')
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('Attrition', axis=1), df['Attrition'], test_size=0.2, random_state=42
    )

    # Train a LightGBM model
    model = LGBMClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save the model
    model_path = f"lgbm_model_{ds}.joblib"
    joblib.dump(model, model_path)

    ti.xcom_push(key='lgbm_model', value={'model_path': model_path, 'accuracy': accuracy})


def train_random_forest(ds, **kwargs):
    ti = kwargs['ti']
    # Load the cleaned data
    df = pd.read_csv("clean_employee_attrition.csv", index_col=0, on_bad_lines='skip')
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('Attrition', axis=1), df['Attrition'], test_size=0.2, random_state=42
    )

    # Train a Random Forest model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save the model
    model_path = f"rf_model_{ds}.joblib"
    joblib.dump(model, model_path)

    ti.xcom_push(key='random_forest_model', value={'model_path': model_path, 'accuracy': accuracy})


def choose_best_model(**kwargs):
    ti = kwargs['ti']
    lgbm_result = ti.xcom_pull(key='lgbm_model', task_ids='ml_train_lgbm')
    rf_result = ti.xcom_pull(key='random_forest_model', task_ids='ml_train_rf')

    model_scores = {
        'lgbm': lgbm_result['accuracy'],
        'random_forest': rf_result['accuracy']
    }

    best_model_key = max(model_scores, key=model_scores.get)
    worst_model_path = rf_result['model_path'] if best_model_key == 'lgbm' else lgbm_result['model_path']
    best_score = model_scores[best_model_key]

    os.remove(worst_model_path)
    print(f"Best Model: {best_model_key} with score {best_score}")
