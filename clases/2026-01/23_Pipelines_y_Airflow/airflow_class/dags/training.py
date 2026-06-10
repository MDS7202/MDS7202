"""Funciones de entrenamiento de modelos de machine learning."""
import logging
import os
import time
from typing import Any

import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

log = logging.getLogger(__name__)


def ml_train_LGBM() -> None:
    """Entrena un LGBMClassifier sobre el dataset limpio e imprime el accuracy.

    Versión simplificada para el pipeline de un solo dataset (sin XCom ni persistencia del modelo).
    Lee ``clean_employee_attrition.csv`` desde el directorio de trabajo.
    """
    df = pd.read_csv("clean_employee_attrition.csv", index_col=0, on_bad_lines="skip")
    log.info("Dataset cargado: %d filas × %d columnas", *df.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        df.drop("Attrition", axis=1), df["Attrition"], test_size=0.2, random_state=42
    )
    log.info(
        "Partición entrenamiento/prueba: %d / %d muestras", len(X_train), len(X_test)
    )

    log.info("Iniciando entrenamiento LightGBM...")
    t0 = time.perf_counter()
    model = LGBMClassifier()
    model.fit(X_train, y_train)
    elapsed = time.perf_counter() - t0
    log.info("Entrenamiento completado en %.2f s", elapsed)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    log.info("Accuracy en test: %.4f", accuracy)


def train_lgbm(ds: str) -> dict[str, Any]:
    """Entrena un LGBMClassifier y devuelve las métricas y la ruta del modelo guardado.

    Args:
        ds: Fecha de ejecución del DAG (``YYYY-MM-DD``), usada para nombrar el archivo del modelo.

    Returns:
        dict con ``model_path`` (str) y ``accuracy`` (float). Con TaskFlow API,
        este valor se propaga automáticamente al XCom y a las tareas descendentes.
    """
    df = pd.read_csv("clean_employee_attrition.csv", index_col=0, on_bad_lines="skip")
    log.info("Dataset cargado: %d filas × %d columnas", *df.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        df.drop("Attrition", axis=1), df["Attrition"], test_size=0.2, random_state=42
    )
    log.info(
        "Partición entrenamiento/prueba: %d / %d muestras", len(X_train), len(X_test)
    )

    log.info("Iniciando entrenamiento LightGBM...")
    t0 = time.perf_counter()
    model = LGBMClassifier()
    model.fit(X_train, y_train)
    elapsed = time.perf_counter() - t0
    log.info("Entrenamiento completado en %.2f s", elapsed)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    log.info("Accuracy en test: %.4f", accuracy)

    model_path = f"lgbm_model_{ds}.joblib"
    joblib.dump(model, model_path)
    size_kb = os.path.getsize(model_path) / 1024
    log.info("Modelo guardado en '%s' (%.1f KB)", model_path, size_kb)

    return {"model_path": model_path, "accuracy": accuracy}


def train_random_forest(ds: str) -> dict[str, Any]:
    """Entrena un RandomForestClassifier y devuelve las métricas y la ruta del modelo guardado.

    Args:
        ds: Fecha de ejecución del DAG (``YYYY-MM-DD``), usada para nombrar el archivo del modelo.

    Returns:
        dict con ``model_path`` (str) y ``accuracy`` (float). Con TaskFlow API,
        este valor se propaga automáticamente al XCom y a las tareas descendentes.
    """
    df = pd.read_csv("clean_employee_attrition.csv", index_col=0, on_bad_lines="skip")
    log.info("Dataset cargado: %d filas × %d columnas", *df.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        df.drop("Attrition", axis=1), df["Attrition"], test_size=0.2, random_state=42
    )
    log.info(
        "Partición entrenamiento/prueba: %d / %d muestras", len(X_train), len(X_test)
    )

    log.info("Iniciando entrenamiento Random Forest...")
    t0 = time.perf_counter()
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    elapsed = time.perf_counter() - t0
    log.info("Entrenamiento completado en %.2f s", elapsed)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    log.info("Accuracy en test: %.4f", accuracy)

    model_path = f"rf_model_{ds}.joblib"
    joblib.dump(model, model_path)
    size_kb = os.path.getsize(model_path) / 1024
    log.info("Modelo guardado en '%s' (%.1f KB)", model_path, size_kb)

    return {"model_path": model_path, "accuracy": accuracy}
