"""Ejemplo de callbacks en Airflow: notificaciones de éxito y fallo.

Los callbacks permiten ejecutar lógica personalizada cuando una tarea o el DAG completo
cambian de estado. Son la base de los sistemas de alertas en producción.

Hay tres niveles de callback:
- ``on_success_callback`` / ``on_failure_callback`` en ``default_args`` → aplican a todas las tareas.
- ``on_success_callback`` / ``on_failure_callback`` en un operador individual → solo esa tarea.
- ``on_failure_callback`` en ``@dag`` → se dispara si el DAG termina en estado fallido.

En producción los callbacks suelen enviar mensajes a Slack, PagerDuty o email.
Aquí se simulan con logs estructurados para que sea fácil ver el comportamiento en la UI.
"""
import logging
from datetime import timedelta

import pendulum
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.context import Context

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Funciones de callback
# ---------------------------------------------------------------------------

def notificar_fallo_tarea(context: Context) -> None:
    """Callback ejecutado cuando una tarea individual falla.

    Args:
        context: Contexto de ejecución de Airflow con información de la tarea y el DAG.
    """
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    execution_date = context["execution_date"]
    exception = context.get("exception", "desconocido")
    log_url = context["task_instance"].log_url

    log.error(
        "\n[ALERTA — TAREA FALLIDA]\n"
        "  DAG:    %s\n"
        "  Tarea:  %s\n"
        "  Fecha:  %s\n"
        "  Error:  %s\n"
        "  Logs:   %s",
        dag_id, task_id, execution_date, exception, log_url,
    )
    # En producción: reemplazar por una llamada real, por ejemplo:
    # slack_sdk.WebClient(token=Variable.get("slack_token")).chat_postMessage(
    #     channel="#alertas-mlops",
    #     text=f":red_circle: *{dag_id} / {task_id}* falló el {execution_date}",
    # )


def notificar_exito_tarea(context: Context) -> None:
    """Callback ejecutado cuando una tarea individual finaliza con éxito.

    Args:
        context: Contexto de ejecución de Airflow.
    """
    task_id = context["task_instance"].task_id
    duration = context["task_instance"].duration
    log.info("[OK] Tarea '%s' completada en %.2f s", task_id, duration or 0)


def notificar_fallo_dag(context: Context) -> None:
    """Callback ejecutado cuando el DAG completo termina en estado fallido.

    Se configura en el decorador ``@dag``, no en ``default_args``.

    Args:
        context: Contexto de ejecución de Airflow.
    """
    dag_id = context["dag"].dag_id
    execution_date = context["execution_date"]
    log.error(
        "\n[CRÍTICO — DAG FALLIDO]\n"
        "  DAG:    %s\n"
        "  Fecha:  %s\n"
        "  Acción: revisar tareas fallidas y reintentar si corresponde.",
        dag_id, execution_date,
    )


# ---------------------------------------------------------------------------
# DAG
# ---------------------------------------------------------------------------

args = {
    "owner": "MDS7202",
    "retries": 1,
    "retry_delay": timedelta(seconds=30),   # espera 30 s antes de reintentar
    "on_failure_callback": notificar_fallo_tarea,
    "on_success_callback": notificar_exito_tarea,
}


@dag(
    dag_id="ejemplo_callbacks",
    default_args=args,
    description="Demuestra on_failure_callback y on_success_callback a nivel de tarea y de DAG",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    on_failure_callback=notificar_fallo_dag,
)
def ejemplo_callbacks():
    # Las dos tareas corren en paralelo para mostrar ambos callbacks a la vez.
    # 'fin' usa trigger_rule="all_done" para ejecutarse siempre, sin importar
    # si alguna tarea anterior falló.
    inicio = EmptyOperator(task_id="inicio")
    fin = EmptyOperator(task_id="fin", trigger_rule="all_done")

    @task
    def tarea_exitosa() -> str:
        """Siempre termina correctamente; dispara on_success_callback."""
        log.info("Procesamiento completado sin errores.")
        return "resultado_ok"

    @task
    def tarea_fallida() -> None:
        """Siempre lanza una excepción; dispara on_failure_callback."""
        raise ValueError("Error de ejemplo: fallo intencional para demostrar el callback.")

    inicio >> [tarea_exitosa(), tarea_fallida()] >> fin


ejemplo_callbacks()
