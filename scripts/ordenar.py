import main
import csv

def asc_desc(campo:str):
    while True:
        opcion = main.ingresar_opcion("\nOrdenar de forma Ascendente o Descendente? " \
        "(1: Ascendente, 2: Descendente, 0: volver al menú ordenar): ", rango_max=2)
        if (opcion in [1, 2]):
            break
        elif (opcion == 0):
            return
        
    path_cargados = main.configuracion["Paises"]["Paises_Cargados"]
    codificacion = main.configuracion["Configuracion"]["codificacion"]
    contenido_ordenado = []

    with open(path_cargados, "r", encoding=codificacion, newline="") as cargados_archivo:
        lector_cargados = csv.reader(cargados_archivo)
        cabecera = next(lector_cargados)
        print(f"\n--- Paises ordenados por {campo} de forma " \
        f"{"Ascendente" if opcion == 1 else "Descendente"} ---")
        orden = True if opcion == 2 else False
        if (campo in ["población", "superficie"]):
            contenido_ordenado = sorted(lector_cargados, key=lambda 
                                    x: int(x[cabecera.index(campo)]), reverse=orden)
        elif (campo == "nombre"):
            contenido_ordenado = sorted(lector_cargados, key=lambda 
                                    x: x[cabecera.index(campo)], reverse=orden)
        for pais in contenido_ordenado:
            print(pais)
    
    with open(path_cargados, "w", encoding=codificacion, newline="") as cargados_archivo:
        cargados_archivo.write(",".join(cabecera))
        if contenido_ordenado:
            for pais in contenido_ordenado:
                cargados_archivo.write("\n" + ",".join(pais))