"""Modulo API: acceso a los datos del Excel y logica de consulta.

No imprime ni pide nada al usuario (eso es trabajo del modulo ui).
"""
import difflib
import os

import pandas as pd

from api.limpieza import (limpiar_fosforo, limpiar_ph, limpiar_potasio,
                          normalizar)

RUTA_EXCEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "data", "resultado_laboratorio_suelo.xlsx")


COLUMNAS_TEXTO = ["Departamento", "Municipio", "Cultivo", "Topografia"]
VARIABLES = {"pH": "pH", "P": "Fosforo (P) mg/kg", "K": "Potasio (K) cmol(+)/kg"}


def _columna_usada(nombre):
    """Filtro por nombre, no por posicion"""
    return (nombre in COLUMNAS_TEXTO
            or nombre.startswith("pH agua")
            or nombre.startswith("Fosforo (P)")
            or nombre.startswith("Potasio (K)"))


def cargar_datos(ruta=RUTA_EXCEL):
    """limpia pH/P/K y devuelve un DataFrame listo"""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontro el archivo de datos: {ruta}")
    crudo = pd.read_excel(ruta, usecols=_columna_usada, dtype=object)

    datos = pd.DataFrame()
    for col in COLUMNAS_TEXTO:
        datos[col] = crudo[col].astype(str).str.strip()
        datos[col + "_n"] = datos[col].map(normalizar)   
    col_ph = next(c for c in crudo.columns if c.startswith("pH agua"))
    col_p = next(c for c in crudo.columns if c.startswith("Fosforo (P)"))
    col_k = next(c for c in crudo.columns if c.startswith("Potasio (K)"))
    datos["pH"] = crudo[col_ph].map(limpiar_ph)
    datos["P"] = crudo[col_p].map(limpiar_fosforo)
    datos["K"] = crudo[col_k].map(limpiar_potasio)
    return datos


def valores_disponibles(datos, columna, departamento=None, municipio=None):

    sub = datos
    if departamento:
        sub = sub[sub["Departamento_n"] == normalizar(departamento)]
    if municipio:
        sub = sub[sub["Municipio_n"] == normalizar(municipio)]
    return sorted(sub[columna].unique())


def sugerencias(texto, opciones, max_sugerencias=3):
    
    mapa = {normalizar(o): o for o in opciones}
    cercanas = difflib.get_close_matches(normalizar(texto), list(mapa), n=max_sugerencias, cutoff=0.6)
    return [mapa[c] for c in cercanas]


def consultar(datos, departamento, municipio, cultivo, n_registros):
    
    filtro = ((datos["Departamento_n"] == normalizar(departamento))
              & (datos["Municipio_n"] == normalizar(municipio))
              & (datos["Cultivo_n"] == normalizar(cultivo)))
    return datos[filtro].head(n_registros)


def medianas_por_topografia(registros):
    """Una fila por topografia + una fila 'TODAS' con la mediana de pH, P y K.

    Cada fila trae tambien cuantos registros tenian valor valido de cada variable.
    """
    filas = []
    grupos = [(topo, sub) for topo, sub in registros.groupby("Topografia", sort=True)]
    if len(grupos) > 1:                      # con una sola topografia 'TODAS' seria repetido
        grupos.append(("TODAS", registros))
    for topo, sub in grupos:
        fila = {
            "Departamento": registros["Departamento"].iloc[0],
            "Municipio": registros["Municipio"].iloc[0],
            "Cultivo": registros["Cultivo"].iloc[0],
            "Topografía": topo,
            "Registros": len(sub),
        }
        for clave in VARIABLES:
            fila[clave] = sub[clave].median()      
        filas.append(fila)
    return filas
