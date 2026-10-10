"""conecta el modulo UI con el modulo API"""
import sys

import api
import ui


def pedir_valido(nombre, opciones):

    validas = {api.normalizar(o): o for o in opciones}
    while True:
        texto = ui.pedir_texto(f"{nombre} (? para ver opciones)", ayuda=opciones)
        if api.normalizar(texto) in validas:
            return validas[api.normalizar(texto)]
        ui.mostrar_error(f"'{texto}' no existe en los datos.", api.sugerencias(texto, opciones))


def consulta(datos):
    """pide los 4 datos, consulta y muestra la tabla"""
    departamento = pedir_valido("Departamento", api.valores_disponibles(datos, "Departamento"))
    municipio = pedir_valido("Municipio", api.valores_disponibles(datos, "Municipio", departamento))
    cultivo = pedir_valido("Cultivo", api.valores_disponibles(datos, "Cultivo", departamento, municipio))
    n = ui.pedir_entero_positivo("Numero de registros a consultar")

    registros = api.consultar(datos, departamento, municipio, cultivo, n)
    if len(registros) < n:
        print(f"  [i] Solo existen {len(registros)} registros (pediste {n}).")
    ui.mostrar_tabla(api.medianas_por_topografia(registros))


def main():
    if hasattr(sys.stdout, "reconfigure"):        
        sys.stdout.reconfigure(encoding="utf-8")
    ui.mostrar_titulo()
    print("Cargando y limpiando datos (puede tardar unos segundos)...")
    try:
        datos = api.cargar_datos()
    except (FileNotFoundError, ValueError) as error:
        ui.mostrar_error(f"No se pudieron cargar los datos: {error}")
        return
    print(f"Listo: {len(datos):,} registros cargados.\n")

    while True:
        consulta(datos)
        if not ui.preguntar_si_no("Hacer otra consulta?"):
            print("Hasta pronto")
            break
        print()


if __name__ == "__main__":
    main()
