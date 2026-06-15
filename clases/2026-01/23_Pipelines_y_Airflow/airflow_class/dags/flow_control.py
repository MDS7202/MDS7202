"""Funciones de control de flujo y bifurcación para los pipelines de Airflow."""
import logging

log = logging.getLogger(__name__)

FECHA_UMBRAL = "2024-06-28"


def choose_data_branch(ds: str) -> list[str]:
    """Selecciona qué datasets descargar según la fecha de ejecución del DAG.

    Antes de la fecha umbral (``2024-06-28``) usa los datasets 1 y 2;
    desde esa fecha en adelante usa los datasets 1 y 3.

    Con TaskFlow API (``@task.branch``), el valor de retorno es directamente la lista
    de task IDs a ejecutar; no se necesita XCom manual.

    Args:
        ds: Fecha de ejecución del DAG en formato ``YYYY-MM-DD``.

    Returns:
        Lista de task IDs a ejecutar (Airflow branching).
    """
    log.info("Fecha de ejecución del DAG: %s", ds)
    log.info("Fecha umbral de bifurcación: %s", FECHA_UMBRAL)

    if ds < FECHA_UMBRAL:
        selected_tasks = ["download_dataset_1", "download_dataset_2"]
        log.info("Fecha anterior al umbral → rama seleccionada: datasets 1 y 2")
    else:
        selected_tasks = ["download_dataset_1", "download_dataset_3"]
        log.info("Fecha igual o posterior al umbral → rama seleccionada: datasets 1 y 3")

    return selected_tasks
