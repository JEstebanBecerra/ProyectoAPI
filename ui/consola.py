"""Módulo UI: todo lo que se muestra o se pide por consola.

No sabe nada del Excel; solo recibe y devuelve datos simples.
"""
import math


def mostrar_titulo():
    print("=" * 64)
    print("  PROPIEDADES EDÁFICAS - Resultados de laboratorio de suelos")
    print("=" * 64)


def pedir_texto(mensaje, ayuda=None):
    """Pide un texto no vacío. Escribir '?' muestra la ayuda (opciones válidas)."""
    while True:
        texto = input(f"{mensaje}: ").strip()
        if texto == "?" and ayuda:
            mostrar_lista("Opciones disponibles", ayuda)
        elif texto:
            return texto
        else:
            print("  [!] No puede estar vacío." + (" Escribe '?' para ver opciones." if ayuda else ""))


def pedir_entero_positivo(mensaje):
    while True:
        texto = input(f"{mensaje}: ").strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("  [!] Escribe un número entero mayor que 0.")


def preguntar_si_no(mensaje):
    return input(f"{mensaje} (s/n): ").strip().lower().startswith("s")


def mostrar_lista(titulo, elementos):
    print(f"\n  {titulo} ({len(elementos)}):")
    for e in elementos:
        print(f"   - {e}")
    print()


def mostrar_error(mensaje, sugeridos=None):
    print(f"  [x] {mensaje}")
    if sugeridos:
        print("    ¿Quisiste decir? " + " | ".join(sugeridos))


def _fmt(valor):
    return "N/D" if valor is None or (isinstance(valor, float) and math.isnan(valor)) else f"{valor:.2f}"


def mostrar_tabla(filas):
    """Imprime la tabla: Departamento, Municipio, Cultivo, Topografía y medianas."""
    columnas = [("Departamento", "Departamento"), ("Municipio", "Municipio"),
                ("Cultivo", "Cultivo"), ("Topografía", "Topografía"),
                ("Registros", "N"), ("pH", "Mediana pH"),
                ("P", "Mediana P (mg/kg)"), ("K", "Mediana K (cmol/kg)")]
    matriz = []
    for f in filas:
        matriz.append([_fmt(f[c]) if c in ("pH", "P", "K") else str(f[c]) for c, _ in columnas])
    anchos = [max(len(t), *(len(fila[i]) for fila in matriz)) for i, (_, t) in enumerate(columnas)]

    linea = "+" + "+".join("-" * (a + 2) for a in anchos) + "+"
    print("\n" + linea)
    print("|" + "|".join(f" {t.center(a)} " for (_, t), a in zip(columnas, anchos)) + "|")
    print(linea)
    for fila in matriz:
        print("|" + "|".join(f" {v.ljust(a)} " if i < 4 else f" {v.rjust(a)} "
                             for i, (v, a) in enumerate(zip(fila, anchos))) + "|")
    print(linea)
    print("  N/D = sin datos válidos (valores '<límite de detección' o 'ND' no se promedian).\n")
