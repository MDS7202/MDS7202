"""Funciones de preprocesamiento de datos para los pipelines de MLOps."""
import logging

import pandas as pd
from airflow.models import Variable

from flow_control import FECHA_UMBRAL

log = logging.getLogger(__name__)


def clean_data(file_path: str, data_key: str | None = None) -> None:
    """Lee un CSV, codifica variables categóricas con one-hot encoding y guarda el resultado.

    Args:
        file_path: Ruta al CSV crudo (soporta plantillas Jinja, e.g. ``"data_{{ ds }}.csv"``).
        data_key: Si se especifica, guarda el DataFrame limpio como Airflow Variable bajo esta clave.
            Útil para pipelines multi-dataset donde tareas posteriores necesitan acceder a los datos
            sin pasar por el sistema de archivos.
    """
    log.info("Cargando archivo: '%s'", file_path)
    df = pd.read_csv(file_path, on_bad_lines="skip")
    log.info("Dataset cargado: %d filas × %d columnas", *df.shape)

    df = df.drop(columns=["Employee ID"])
    X = df.drop(columns=["Attrition"])
    y = df["Attrition"]

    class_dist = y.value_counts().to_dict()
    log.info("Distribución de clases — %s", class_dist)

    categorical_columns = X.select_dtypes(include=["object"]).columns
    log.info(
        "Columnas categóricas a codificar (%d): %s",
        len(categorical_columns),
        list(categorical_columns),
    )

    df_transformed = pd.get_dummies(X, columns=categorical_columns, drop_first=True)
    log.info(
        "Dimensiones tras one-hot encoding: %d filas × %d columnas", *df_transformed.shape
    )

    df_transformed = pd.concat([df_transformed, y], axis=1)
    df_transformed.to_csv("clean_employee_attrition.csv")
    log.info("Dataset limpio guardado en 'clean_employee_attrition.csv'")

    if data_key:
        Variable.set(data_key, df_transformed.to_json())
        log.info("Dataset almacenado como Variable de Airflow con clave: '%s'", data_key)


def join_data(ds: str) -> None:
    """Recupera los datasets limpios de Airflow Variables y los concatena en un solo CSV.

    Recalcula los datasets a combinar a partir de ``ds`` usando la misma lógica
    de ``choose_data_branch``, evitando dependencia de XCom entre tareas.

    Args:
        ds: Fecha de ejecución del DAG (``YYYY-MM-DD``).
    """
    keys = (
        [f"data_1_{ds}", f"data_2_{ds}"]
        if ds < FECHA_UMBRAL
        else [f"data_1_{ds}", f"data_3_{ds}"]
    )

    log.info("Combinando %d datasets: %s", len(keys), keys)

    data_list = []
    for key in keys:
        data = pd.read_json(Variable.get(key))
        log.info("  → Dataset '%s': %d filas × %d columnas", key, *data.shape)
        data_list.append(data)

    df = pd.concat(data_list, axis=0)
    log.info("Dataset combinado: %d filas × %d columnas", *df.shape)

    df.to_csv("clean_employee_attrition.csv")
    log.info("Dataset combinado guardado en 'clean_employee_attrition.csv'")
