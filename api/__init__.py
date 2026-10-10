"""Paquete API: carga, limpieza y consulta de los datos de suelos."""
from api.limpieza import normalizar
from api.suelos import (VARIABLES, cargar_datos, consultar,
                        medianas_por_topografia, sugerencias,
                        valores_disponibles)

__all__ = ["VARIABLES", "cargar_datos", "consultar", "medianas_por_topografia",
           "normalizar", "sugerencias", "valores_disponibles"]
