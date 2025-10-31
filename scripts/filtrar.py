import main, csv, sys

def filtrar_continente():
    while True:
        print("\n--- Filtrar por Continente ---\n"
        "1. África\n"
        "2. América\n"
        "3. Asia\n"
        "4. Europa\n"
        "5. Oceanía\n"
        "0. Volver al menú filtrar")

        opcion = main.ingresar_opcion(rango_max=5)

        continente_nombre = None

        match opcion:
            case 1|2|3|4|5:
                continente_nombre = main.CONTINENTES[opcion - 1]
            case 0:
                break
            case _:
                continue

        path_cargados = main.configuracion["Paises"]["Paises_Cargados"]
        codificacion = main.configuracion["Configuracion"]["codificacion"]
        contador = 0
        with open(path_cargados, "r", encoding=codificacion) as cargados_archivo:
            lector_cargados = csv.reader(cargados_archivo)
            print(f"\n--- Paises de {continente_nombre} ---")
            print(next(lector_cargados))  # Saltar encabezado
            for pais in lector_cargados:
                pais_continente = main.get_atributo(pais, 3)
                if pais_continente == continente_nombre:
                    print(pais)
                    contador += 1
        if contador == 0:
            print(f"- No se encontraron países en {continente_nombre}")

def filtrar_poblacion_o_superficie(opcion:str, indice:int):
    while True:

        min = main.ingresar_opcion(f"\nIngresar mínimo de {opcion} (al menos 1, o 0 " \
        "para volver al menú filtrar): ")

        if min == 0:
            return
        elif min != None:
            break

    while True:
        max = main.ingresar_opcion(f"\nIngresar máximo de {opcion} (mayor o igual " \
        "al mínimo, o 0 para volver al menú filtrar, -1 para máximo Infinito): ", rango_min=-1)

        if max == -1:
            max = sys.maxsize
        elif max == None:
            continue

        if (1 <= max < min):
            print("El máximo debe ser mayor o igual al mínimo " \
            f"(mínimo actual: {min})")

        elif (max >= min):

            path_cargados = main.configuracion["Paises"]["Paises_Cargados"]
            codificacion = main.configuracion["Configuracion"]["codificacion"]
            contador = 0

            with open(path_cargados, "r", encoding=codificacion) as cargados_archivo:
                print(f"\n--- Paises con {opcion} entre {min} y {max} ---")
                lector_cargados = csv.reader(cargados_archivo)
                print(next(lector_cargados))
                for pais in lector_cargados:
                    atributo = int(main.get_atributo(pais, indice))
                    if (min <= atributo <= max):
                        print(pais)
                        contador += 1
            if (contador == 0):
                print(f"- No se encontraron países con {opcion} entre {min} y {max}")
            break
        elif (max == 0):
            break