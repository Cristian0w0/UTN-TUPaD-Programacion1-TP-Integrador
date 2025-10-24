import main

def filtrar_continente(CONTINENTES):
    while True:
        print("\n--- Filtrar por Continente ---\n"
        "1. África\n"
        "2. Asia\n"
        "3. Europa\n"
        "4. América\n"
        "5. Oceanía\n"
        "0. Volver al menú filtrar")
        opcion = main.ingresar_opcion(rango_max=5)
        with open("./paises.csv", "r", encoding="utf-8-sig") as archivo:
            if (opcion == None):
                continue
            elif (1 <= opcion <= 5):
                continente = CONTINENTES[opcion-1]
                print(f"\n--- Paises de {continente} ---")
                for linea in archivo:
                    if (main.get_atributo(linea, 3) == continente):
                        pais = main.get_atributo(linea, 0)
                        print(pais)
            elif (opcion == 0):
                break

def filtrar_poblacion_o_superficie(opcion:str, indice:int):
    while True:
        min = main.ingresar_opcion(f"\nIngresar mínimo de {opcion} (al menos 1, o 0 " \
        "para volver al Menú Filtrar): ")
        if (min == 0):
            return
        elif (min != -1):
            break
    while True:
        max = main.ingresar_opcion(f"\nIngresar máximo de {opcion} (mayor o igual " \
        "al mínimo, 0 para volver al Menú Filtrar, -1 para máximo Infinito): ")
        if (1 <= max < min):
            print("El máximo debe ser mayor o igual al mínimo " \
            f"(mínimo actual: {min})")
        elif (max >= min):
            with open("paises.csv", "r", encoding="utf-8-sig") as archivo:
                print(f"\n--- Paises con {opcion} entre {min} y {max} ---")
                for linea in archivo:
                    atributo = int(main.get_atributo(linea, indice))
                    if (min <= atributo <= max):
                        pais = main.get_atributo(linea, 0)
                        print(f"{pais}", end="")
                        main.print_vacio(len(pais))
                        print(f"{atributo}")
            break
        elif (max == 0):
            break