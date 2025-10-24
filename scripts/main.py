import csv
import sys
import filtrar, ordenar, mostrar

CONTINENTES = ["África", "Asia", "Europa", "América", "Oceanía"]

HEADER = ["nombre", "población", "superficie", "continente", "onu"]

contenido = None

#agregar archivo de config con todos los paths relativos a la carpeta donde se encuentran
#agregar recursividad para encontrar todos los archivos
#agregar validaciones para campos

def main():
    while True:
        print("\n--- Menú Principal ---\n"
        "1. Filtrar países\n"
        "2. Ordenar países\n"
        "3. Mostrar estadísticas\n"
        "4. Cargar países\n"
        "0. Salir")
        opcion = ingresar_opcion(rango_max=3)
        match opcion:
            case 0:
                print("\nSaliendo...")
                break
            case 1:
                menu_filtrar()
            case 2:
                menu_ordenar()
            case 3:
                menu_mostrar()
            case 4:
                menu_cargar()

def menu_filtrar():
    while True:
        print("\n--- Menú Filtrar ---\n"
        "1. Filtrar países por Continente\n"
        "2. Filtrar países por rango de Población\n"
        "3. Filtrar países por rango de Superficie\n"
        "0. Volver al Menú Principal")
        opcion = ingresar_opcion(rango_max=3)
        match opcion:
            case 0:
                break
            case 1:
                filtrar.filtrar_continente(CONTINENTES)
            case 2:
                filtrar.filtrar_poblacion_o_superficie("Población", 1)
            case 3:
                filtrar.filtrar_poblacion_o_superficie("Superficie", 2)

def menu_ordenar():
    while True:
        print("\n--- Menú Ordenar ---\n"
        "1. Ordenar países por Nombre\n"
        "2. Ordenar países por Población\n"
        "3. Ordenar países por Superficie\n"
        "0. Volver al menú principal")
        opcion = ingresar_opcion(rango_max=3)
        match opcion:
            case 0:
                break
            case 1:
                ordenar.asc_desc("nombre")
            case 2:
                ordenar.asc_desc("población")
            case 3:
                ordenar.asc_desc("superficie")

def menu_mostrar():
    print("\n--- Menú Estadísticas ---\n"
    "1. Mostrar país con mayor y menor Población\n"
    "2. Mostrar promedio de Población\n"
    "3. Mostrar promedio de Superficie\n"
    "4. Mostrar cantidad de países por Continente\n"
    "5. Mostrar países cargados\n"
    "0. Volver al menú principal")
    opcion = ingresar_opcion(rango_max=4)

def menu_cargar():
    print("\n--- Menú Cargar ---\n"
    "1. Cargar país por nombre\n"
    "2. Cargar países de continente\n"
    "3. Cargar países reconocidos por la ONU\n"
    "4. Cargar países no reconocidos por la ONU\n"
    "0. Volver al menú principal\n\n")

def ingresar_opcion(texto:str = "\nIngresar opción: ", 
                    rango_max:int = sys.maxsize, rango_min:int = 0):
    try:
        opcion = int(input(texto))
        if (not rango_min <= opcion <= rango_max):
            raise ValueError
    except ValueError:
        print("Opción inválida")
        opcion = None
    finally:
        return opcion

def get_atributo(linea:str, indice:int):
    return linea.strip().split(",")[indice]

def print_vacio(recorte:int):
    print(" " * (40-recorte), end="")

def cargar_contenido():
    pass

if (__name__ == "__main__"):
    main()