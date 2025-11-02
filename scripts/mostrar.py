import main, csv, sys

def mayor_menor_poblacion():
    # Encontrar países con mayor y menor población
    paises_mayor = []
    paises_menor = []
    mayor_poblacion = 0
    menor_poblacion = sys.maxsize
    path_cargados = main.configuracion["Paises"]["Paises_Cargados"]
    codificacion = main.configuracion["Configuracion"]["codificacion"]
    with open(path_cargados, "r", encoding=codificacion, newline="") as cargados_archivo:
        lector_cargados = csv.reader(cargados_archivo)
        cabecera = next(lector_cargados)
        for pais in lector_cargados:
            pais_poblacion = int(main.get_atributo(pais, 1))
            # Buscar país con mayor población
            if pais_poblacion > mayor_poblacion:
                mayor_poblacion = pais_poblacion
                paises_mayor = []
                paises_mayor.append(pais)
            elif pais_poblacion == mayor_poblacion:
                paises_mayor.append(pais)
            # Buscar país con menor población
            elif pais_poblacion < menor_poblacion:
                menor_poblacion = pais_poblacion
                paises_menor = []
                paises_menor.append(pais)
            elif pais_poblacion == menor_poblacion:
                paises_menor.append(pais)
    if 0 in [mayor_poblacion, menor_poblacion]:
        print("\nNo hay países cargados para determinar mayor y menor población.")
    else:
        # Mostrar resultados
        print("\n--- País(es) con mayor población ---")
        print(cabecera)
        for pais in paises_mayor:
            print(pais)
        print("\n--- País(es) con menor población ---")
        print(cabecera)
        for pais in paises_menor:
            print(pais)



def promedio(atributo, indice):
    # Calcular promedio de población o superficie
    path_cargados = main.configuracion["Paises"]["Paises_Cargados"]
    codificacion = main.configuracion["Configuracion"]["codificacion"]
    with open(path_cargados, "r", encoding=codificacion, newline="") as cargados_archivo:
        lector_cargados = csv.reader(cargados_archivo)
        next(lector_cargados)
        total_suma = 0
        total_paises = 0
        # Sumar todos los valores del atributo
        for pais in lector_cargados:
            total_suma += int(main.get_atributo(pais, indice))
            total_paises += 1
    # Calcular y mostrar promedio
    promedio = total_suma / total_paises if total_paises > 0 else 0
    print(f"\n--- Promedio de {atributo} de los países cargados: {promedio:.2f} ---")



def paises_por_continente():
    # Contar países por continente
    path_cargados = main.configuracion["Paises"]["Paises_Cargados"]
    codificacion = main.configuracion["Configuracion"]["codificacion"]
    # Inicializar diccionario para contar países por continente
    continentes = {contiente :0 for contiente in main.CONTINENTES}
    with open(path_cargados, "r", encoding=codificacion, newline="") as cargados_archivo:
        lector_cargados = csv.reader(cargados_archivo)
        next(lector_cargados)
        for pais in lector_cargados:
            pais_continente = main.get_atributo(pais, 3)
            continentes[pais_continente] += 1
    # Mostrar estadísticas por continente
    print("\n--- Países por continente ---")
    for continente, paises in continentes.items():
        print(f"{continente}: {paises} países")



def mostrar_cargados():
    # Mostrar todos los países cargados actualmente
    path_cargados = main.configuracion["Paises"]["Paises_Cargados"]
    codificacion = main.configuracion["Configuracion"]["codificacion"]
    with open(path_cargados, "r", encoding=codificacion, newline="") as cargados_archivo:
        lector_cargados = csv.reader(cargados_archivo)
        cabecera = next(lector_cargados)
        print("\n--- Países cargados ---")
        print(cabecera)
        contador_paises = 0
        # Mostrar cada país
        for pais in lector_cargados:
            print(pais)
            contador_paises += 1
    if contador_paises == 0:
        print("No hay países cargados para mostrar.")