"""Funciones de limpieza de datos del archivo de laboratorio de suelos

"""
import math
import re
import unicodedata
from datetime import date, datetime

NAN = float("nan")


RANGO_PH = (3.0, 11.0)
RANGO_P = (0.0, 1000.0)      # mg/kg
RANGO_K = (0.0, 20.0)        # cmol(+)/kg


def normalizar(texto):
    """Mayusculas, sin tildes ni signos y con espacios simples.

    Permite comparar 'Santa Rosa de Cabal' con 'SANTA ROSA DE CABAL'.
    """
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^A-Za-z0-9]+", " ", texto)
    return texto.strip().upper()


def _a_numero(valor):
    """Convierte str/int/float a float; devuelve None si no es un numero usable."""
    if isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return None if (isinstance(valor, float) and math.isnan(valor)) else valor
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")
        if not texto or texto.startswith("<") or texto.upper() == "ND":
            return None                       
        try:
            return float(texto)
        except ValueError:
            return None
    return None


def _en_rango(x, rango):
    return x if (x is not None and rango[0] < x <= rango[1]) else NAN


def _digitos(n):
    return len(str(abs(int(n))))


def limpiar_ph(valor):
    """pH. Las fechas se invierten: dd/mm -> dd + mm/100."""
    if isinstance(valor, (datetime, date)):
        return _en_rango(valor.day + valor.month / 100, RANGO_PH)
    return _en_rango(_a_numero(valor), RANGO_PH)


def limpiar_fosforo(valor):
   
    if isinstance(valor, (datetime, date)):
        return NAN                            
    x = _a_numero(valor)
    if x is None:
        return NAN
    if float(x).is_integer() and not isinstance(valor, str):
        n = int(x)
        largo = _digitos(n)
        if largo <= 3:
            x = float(n)
        elif largo <= 6:
            x = n / 1e3
        elif largo <= 16:
            x = n / 10 ** (largo - 1)
        else:
            x = n / 1e15
    return _en_rango(float(x), RANGO_P)


def limpiar_potasio(valor):
    """Potasio intercambiable (cmol(+)/kg).

    Los enteros son el valor '0.xxxx' sin el '0.': K = N / 10^(cantidad de digitos).
    Un entero de 1 digito (1, 2, 3) se deja tal cual.
    """
    if isinstance(valor, (datetime, date)):
        return NAN
    x = _a_numero(valor)
    if x is None:
        return NAN
    if float(x).is_integer() and not isinstance(valor, str):
        n = int(x)
        largo = _digitos(n)
        x = float(n) if largo == 1 else n / 10 ** largo
    return _en_rango(float(x), RANGO_K)
