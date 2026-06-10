"""Funciones de evaluación y selección de modelos entrenados."""
import logging
import os
from typing import Any

log = logging.getLogger(__name__)


def choose_best_model(
    lgbm_result: dict[str, Any] | None,
    rf_result: dict[str, Any] | None,
) -> None:
    """Compara los modelos entrenados y elimina del disco el de menor accuracy.

    Con TaskFlow API los resultados llegan directamente como parámetros (sin XCom manual).
    Si solo uno de los modelos se ejecutó (por ``trigger_rule="one_success"`` aguas arriba),
    el parámetro del modelo ausente será ``None``.

    Args:
        lgbm_result: dict con ``model_path`` y ``accuracy`` del modelo LightGBM, o ``None``.
        rf_result: dict con ``model_path`` y ``accuracy`` del modelo Random Forest, o ``None``.

    Raises:
        ValueError: Si ambos parámetros son ``None``.
    """
    model_scores: dict[str, float] = {}
    if lgbm_result:
        model_scores["lgbm"] = lgbm_result["accuracy"]
        log.info("LightGBM      → accuracy: %.4f", lgbm_result["accuracy"])
    else:
        log.warning("No se recibieron resultados de LightGBM")

    if rf_result:
        model_scores["random_forest"] = rf_result["accuracy"]
        log.info("Random Forest → accuracy: %.4f", rf_result["accuracy"])
    else:
        log.warning("No se recibieron resultados de Random Forest")

    if not model_scores:
        raise ValueError("Ningún modelo produjo resultados")

    if len(model_scores) == 2:
        margin = abs(model_scores["lgbm"] - model_scores["random_forest"])
        log.info("Diferencia de accuracy entre modelos: %.4f", margin)

    best_model_key = max(model_scores, key=model_scores.get)  # type: ignore[arg-type]
    best_score = model_scores[best_model_key]
    log.info("Mejor modelo: '%s' (accuracy=%.4f)", best_model_key, best_score)

    if best_model_key == "lgbm" and rf_result:
        os.remove(rf_result["model_path"])
        log.info("Modelo descartado eliminado: '%s'", rf_result["model_path"])
    elif best_model_key == "random_forest" and lgbm_result:
        os.remove(lgbm_result["model_path"])
        log.info("Modelo descartado eliminado: '%s'", lgbm_result["model_path"])
