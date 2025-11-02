import main, csv

def cargar_pais(configuracion):
    # Cargar un país individual por nombre
    codificacion = configuracion["Configuracion"]["codificacion"]
    path_cargados = configuracion["Paises"]["Paises_Cargados"]
    
    while True:
        nombre_pais = input("\nIngresar nombre del país a cargar (o '0' para volver al menú cargar): ").strip()
        if nombre_pais == "0":
            break

        # Verificar si el país ya está cargado
        paises_ya_cargados = set()
        try:
            with open(path_cargados, "r", encoding=codificacion, newline="") as archivo:
                lector = csv.reader(archivo)
                next(lector, None)
                for fila in lector:
                    if fila and len(fila) > 0:
                        nombre_pais_cargado = fila[0].strip().capitalize()
                        paises_ya_cargados.add(nombre_pais_cargado)
        except FileNotFoundError:
            pass

        if nombre_pais.capitalize() in paises_ya_cargados:
            print(f"\nEl país {nombre_pais} ya está cargado.")
            continue

        print(f"\nBuscando {nombre_pais} en continentes...")
        
        # Obtener rutas de archivos de continentes
        continentes_rutas = {}
        for continente in main.CONTINENTES:
            continentes_rutas[continente] = configuracion["Continentes"][main.remover_tildes(continente)]

        # Buscar el país en todos los continentes
        pais_encontrado = None
        continente_encontrado = None
        for continente, ruta in continentes_rutas.items():
            try:
                with open(ruta, "r", encoding=codificacion, newline="") as archivo:
                    lector = csv.reader(archivo)
                    next(lector, None)
                    
                    for fila in lector:
                        if fila and len(fila) > 0:
                            nombre_pais_archivo = fila[0].strip().capitalize()
                            if nombre_pais_archivo == nombre_pais.capitalize():
                                pais_encontrado = fila
                                continente_encontrado = continente
                                break
                    if pais_encontrado:
                        break
            except FileNotFoundError:
                continue

        # Cargar el país si se encontró
        if pais_encontrado:
            with open(path_cargados, "a", encoding=codificacion, newline="") as archivo:
                archivo.write("\n" + ",".join(pais_encontrado))
            print(f"País {nombre_pais} cargado correctamente desde {continente_encontrado}.")
        else:
            print(f"El país {nombre_pais} no se encontró en los archivos de continentes.")



def cargar_continente(configuracion):
    # Cargar todos los países de un continente
    while True:
        print("\n--- Cargar paises por Continente ---\n"
        "1. Cargar África\n"
        "2. Cargar América\n"
        "3. Cargar Asia\n"
        "4. Cargar Europa\n"
        "5. Cargar Oceanía\n"
        "0. Volver al menú cargar")
        opcion = main.ingresar_opcion(rango_max=5)
        path_continente = ""
        match opcion:
            case 0:
                break
            case 1|2|3|4|5:
                path_continente = configuracion["Continentes"][main.remover_tildes(main.CONTINENTES[opcion - 1])]
            case _:
                continue
        
        path_paises_cargados = configuracion["Paises"]["Paises_Cargados"]
        codificacion = configuracion["Configuracion"]["codificacion"]
        nombre_continente = path_continente.split("\\")[-1].split(".")[0].capitalize()
        print(f"\nCargando países de {nombre_continente}...")

        # Obtener lista de países ya cargados
        paises_ya_cargados = set()
        try:
            with open(path_paises_cargados, "r", encoding=codificacion, newline="") as archivo:
                lector = csv.reader(archivo)
                next(lector, None)
                for fila in lector:
                    if fila and len(fila) > 0:
                        nombre_pais = fila[0].strip().capitalize()
                        paises_ya_cargados.add(nombre_pais)
        except FileNotFoundError:
            pass

        # Cargar países del continente seleccionado
        with open(path_continente, "r", encoding=codificacion, newline="") as continente_archivo, \
            open(path_paises_cargados, "a", encoding=codificacion, newline="") as paises_archivo:
            
            lector_paises_entrantes = csv.reader(continente_archivo)
            next(lector_paises_entrantes)
            contador_cargados = 0
            contador_dubplicados = 0

            for pais_entrante in lector_paises_entrantes:
                if not pais_entrante:
                    continue
                
                pais_entrante_nombre = main.get_atributo(pais_entrante, 0).capitalize()
                
                # Evitar duplicados
                if pais_entrante_nombre in paises_ya_cargados:
                    print(f"El país {pais_entrante_nombre} ya está cargado, saltando...")
                    contador_dubplicados += 1
                else:
                    paises_archivo.write("\n" + ",".join(pais_entrante))
                    paises_ya_cargados.add(pais_entrante_nombre)
                    print(f"País {pais_entrante_nombre} cargado correctamente.")
                    contador_cargados += 1

            print(f"\nPaíses nuevos cargados: {contador_cargados}")
            print(f"Países duplicados omitidos: {contador_dubplicados}")



def cargar_onu(configuracion, estado_onu):
    # Cargar países según su estado ONU (reconocidos o no reconocidos)
    estado_texto = "reconocidos por la ONU" if estado_onu == "true" else "no reconocidos por la ONU"

    while True:
        confirmar = main.ingresar_opcion(f"\n¿Seguro que desea cargar todos los países {estado_texto}? " \
                                        "(1: Sí, 0: No, volver al menú cargar): ", rango_max=1)
        if confirmar == 1:
            break
        elif confirmar == 0:
            return

    codificacion = configuracion["Configuracion"]["codificacion"]
    path_cargados = configuracion["Paises"]["Paises_Cargados"]
    
    print(f"\nCargando países {estado_texto}...")

    # Obtener países ya cargados
    paises_ya_cargados = set()
    try:
        with open(path_cargados, "r", encoding=codificacion, newline="") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)
            for fila in lector:
                if fila and len(fila) > 0:
                    nombre_pais = fila[0].strip().capitalize()
                    paises_ya_cargados.add(nombre_pais)
    except FileNotFoundError:
        pass

    # Buscar países por estado ONU en todos los continentes
    continentes_rutas = {}
    for continente in main.CONTINENTES:
        continentes_rutas[continente] = configuracion["Continentes"][main.remover_tildes(continente)]

    paises_para_cargar = []
    paises_encontrados_por_continente = {}

    for continente, ruta in continentes_rutas.items():
        try:
            with open(ruta, "r", encoding=codificacion, newline="") as archivo:
                lector = csv.reader(archivo)
                next(lector, None)
                
                for fila in lector:
                    if fila and len(fila) >= 5:
                        nombre_pais = fila[0].strip().capitalize()
                        pais_onu = fila[4].strip().lower() if len(fila) > 4 else ""
                        
                        # Filtrar por estado ONU y evitar duplicados
                        if pais_onu == estado_onu and nombre_pais not in paises_ya_cargados:
                            paises_para_cargar.append(fila)
                            if continente not in paises_encontrados_por_continente:
                                paises_encontrados_por_continente[continente] = 0
                            paises_encontrados_por_continente[continente] += 1
                            
        except FileNotFoundError:
            print(f"\nArchivo de {continente} no encontrado, saltando...")
            continue

    # Cargar países encontrados
    if paises_para_cargar:
        with open(path_cargados, "a", encoding=codificacion, newline="") as archivo:
            for pais in paises_para_cargar:
                archivo.write("\n" + ",".join(pais))
        
        print(f"Países nuevos cargados: {len(paises_para_cargar)}")
        for continente, cantidad in paises_encontrados_por_continente.items():
            print(f"{continente}: {cantidad} países")
    else:
        print(f"No se encontraron países {estado_texto} nuevos para cargar.")



def introducir_pais(configuracion):
    # Agregar un país manualmente a un continente
    codificacion = configuracion["Configuracion"]["codificacion"]

    while True:
        print("\n--- Introducir país manualmente a continente ---\n"
        "Ingrese los datos del país separados por comas en el siguiente orden:\n"
        "nombre,población,superficie,continente,onu\n"
        "Ejemplo: Argentina,45195777,2780400,América,true\n"
        "Ingrese '0' para volver al menú cargar.")
        
        pais_nuevo = input("\nIngresar datos del país: ").strip()
        if pais_nuevo == "0":
            break

        campos_pais = [campo.strip() for campo in pais_nuevo.split(",")]
        
        # Obtener rutas de archivos de continentes
        continentes_rutas = {}
        for continente_nombre in main.CONTINENTES:
            continentes_rutas[continente_nombre] = configuracion["Continentes"][main.remover_tildes(continente_nombre)]

        # Verificar países existentes en cada continente
        paises_existentes = {}
        try:
            for continente_nombre, path_continente in continentes_rutas.items():
                paises_existentes[continente_nombre] = set()
                with open(path_continente, "r", encoding=codificacion, newline="") as continente_archivo:
                    lector_continente = csv.reader(continente_archivo)
                    next(lector_continente, None)
                    for pais in lector_continente:
                        pais_nombre = main.get_atributo(pais, 0)
                        paises_existentes[continente_nombre].add(pais_nombre)
        except FileNotFoundError:
            pass
        
        pais_nuevo_nombre = main.get_atributo(campos_pais, 0)
        # Validar el país antes de agregarlo
        valido_o_error = validar_pais(campos_pais, paises_existentes)
        if valido_o_error == True:
            pais_nuevo_continente = main.get_atributo(campos_pais, 3)
            with open(continentes_rutas[pais_nuevo_continente], "a", encoding=codificacion, newline="") as continente_archivo:
                continente_archivo.write("\n" + ",".join(campos_pais))
            print(f"País {pais_nuevo_nombre} introducido a {pais_nuevo_continente} correctamente.")
        elif isinstance(valido_o_error, str):
            print(f"No se pudo introducir ({valido_o_error}).")



def limpiar_cargados(configuracion):
    # Limpiar todos los países cargados
    while True:
        opcion = main.ingresar_opcion("\n¿Seguro que desea eliminar todos los países cargados? " \
                                    "(1: Sí, 0: No, volver al menú cargar): ", rango_max=1)
        if opcion == 1:
            break
        elif opcion == 0:
            return

    path_cargados = configuracion["Paises"]["Paises_Cargados"]
    codificacion = configuracion["Configuracion"]["codificacion"]
    
    try:
        # Limpiar archivo manteniendo solo la cabecera
        with open(path_cargados, "r", encoding=codificacion, newline="") as archivo:
            lector = csv.reader(archivo)
            cabecera = next(lector, None)
        
        if cabecera:
            with open(path_cargados, "w", encoding=codificacion, newline="") as archivo:
                archivo.write(",".join(cabecera))
            print("\nSe limpiaron los paises cargados.")
        else:
            with open(path_cargados, "w", encoding=codificacion, newline="") as archivo:
                cabecera_default = main.HEADER
                archivo.write(",".join(cabecera_default))
            print("\nArchivo para paises cargados creado con cabecera por defecto.")
            
    except FileNotFoundError:
        # Crear archivo si no existe
        with open(path_cargados, "w", encoding=codificacion, newline="") as archivo:
            cabecera_default = main.HEADER
            archivo.write(",".join(cabecera_default))
        print("\nArchivo paises_cargados creado (no existía previamente).")
    
    except Exception as e:
        print(f"\nError al limpiar el archivo: {e}")



def limpiar_y_extraer(configuracion):
    # Proceso completo de extracción y validación desde archivo principal
    while True:
        print("\n--- Extraer y limpiar países ---\n"
        "Este proceso validará y extraerá los países del archivo de 'países sin extraer', limpiando todos los otros archivos de datos.")
        confirmar = main.ingresar_opcion("\n¿Seguro que desea continuar? (1: Sí, 0: No): ", rango_max=1)
        if confirmar == 1:
            print("\nLimpiando archivos y extrayendo países...")
            break
        elif confirmar == 0:
            return

    path_sin_extraer = configuracion["Paises"]["Paises_Sin_Extraer"]
    path_cargados = configuracion["Paises"]["Paises_Cargados"]
    codificacion = configuracion["Configuracion"]["codificacion"]

    # Preparar archivos de continentes
    continentes_rutas = {}
    for continente in main.CONTINENTES:
        continentes_rutas[continente] = configuracion["Continentes"][main.remover_tildes(continente)]
    
    paises_existentes = {}

    with open(path_sin_extraer, "r", encoding=codificacion, newline="") as sin_extraer_archivo:
        contenido_sin_extraer = csv.reader(sin_extraer_archivo)
        cabecera = next(contenido_sin_extraer)
    
    # Inicializar archivos de continentes
    for continente_nombre, path_continente in continentes_rutas.items():
        paises_existentes[continente_nombre] = set()
        try:
            with open(path_continente, "r", encoding=codificacion, newline="") as continente_archivo:
                lector_continente = csv.reader(continente_archivo)
                primera_linea = next(lector_continente, None)
                if primera_linea:
                    for pais in lector_continente:
                        if pais and len(pais) > 0:
                            pais_nombre = main.get_atributo(pais, 0)
                            paises_existentes[continente_nombre].add(pais_nombre)
                else:
                    with open(path_continente, "w", encoding=codificacion, newline="") as continente_archivo:
                        continente_archivo.write(",".join(cabecera))
        except FileNotFoundError:
            with open(path_continente, "w", encoding=codificacion, newline="") as continente_archivo:
                continente_archivo.write(",".join(cabecera))
        except StopIteration:
            with open(path_continente, "w", encoding=codificacion, newline="") as continente_archivo:
                continente_archivo.write(",".join(cabecera))

    # Procesar países sin extraer
    with open(path_sin_extraer, "r", encoding=codificacion, newline="") as sin_extraer_archivo, \
        open(path_cargados, "w", encoding=codificacion, newline="") as cargados_archivo:
        
        contenido_sin_extraer = csv.reader(sin_extraer_archivo)
        cabecera = next(contenido_sin_extraer)
        # Obtener índices de columnas
        indice_nombre = cabecera.index("nombre")
        indice_poblacion = cabecera.index("población")
        indice_superficie = cabecera.index("superficie")
        indice_continente = cabecera.index("continente")
        indice_onu = cabecera.index("onu")

        cargados_archivo.write(",".join(cabecera))

        paises_para_continentes = {continente: [] for continente in continentes_rutas.keys()}
        paises_invalidos = []
        contador_cargados = 0

        # Validar y clasificar cada país
        for pais in contenido_sin_extraer:
            pais_nombre = pais[indice_nombre].capitalize()
            pais_poblacion = pais[indice_poblacion]
            pais_superficie = pais[indice_superficie]
            pais_continente = pais[indice_continente].capitalize()
            pais_onu = pais[indice_onu].lower()

            campos_pais = [pais_nombre, pais_poblacion, pais_superficie, pais_continente, pais_onu]
            
            valido_o_error = validar_pais(campos_pais, paises_existentes)
            if valido_o_error == True:
                if pais_continente in paises_para_continentes:
                    paises_para_continentes[pais_continente].append(campos_pais)
                    paises_existentes[pais_continente].add(pais_nombre)
                    print(f"País {pais_nombre} validado correctamente, extrayendo a {pais_continente}...")
                    contador_cargados += 1
            elif isinstance(valido_o_error, str):
                paises_invalidos.append(campos_pais)
                print(f"País {pais_nombre} inválido ({valido_o_error}), saltar país...")

    # Guardar países en sus respectivos continentes
    for continente_nombre, paises in paises_para_continentes.items():
        if paises:
            with open(continentes_rutas[continente_nombre], "a", encoding=codificacion, newline="") as continente_archivo:
                for pais in paises:
                    continente_archivo.write("\n" + ",".join(pais))

    # Guardar países inválidos de vuelta al archivo sin extraer
    with open(path_sin_extraer, "w", encoding=codificacion, newline="") as sin_extraer_archivo:
        sin_extraer_archivo.write(",".join(cabecera))
        for pais in paises_invalidos:
            sin_extraer_archivo.write("\n" + ",".join(pais))

    print(f"\nPaíses válidos extraídos: {contador_cargados}")
    for continente_nombre, paises in paises_para_continentes.items():
        print(f"{continente_nombre}: {len(paises)} países extraidos")
    print(f"Países inválidos: {len(paises_invalidos)}")



def validar_pais(campos_pais: list, paises_existentes: dict):
    # Función de validación completa para un país

    # Validar cantidad de campos
    if len(campos_pais) != 5:
        return f"Cantidad de campos incorrecta. Esperados: 5, Encontrados: {len(campos_pais)}"
    
    pais_nombre = campos_pais[0]
    pais_poblacion = campos_pais[1]
    pais_superficie = campos_pais[2]
    pais_continente = campos_pais[3]
    pais_onu = campos_pais[4]
    
    # Validar campos obligatorios no vacíos
    if "" in campos_pais:
        return "Al menos un campo obligatorio vacío"
    
    # Validar continente existente
    if pais_continente not in paises_existentes:
        return f"Continente '{pais_continente}' no válido"
    
    # Validar país duplicado en continente
    if pais_nombre in paises_existentes[pais_continente]:
        return f"País '{pais_nombre}' ya existe en {pais_continente}"
    
    # Validar nombre (sin números y solo caracteres permitidos)
    if any(letra.isdigit() for letra in pais_nombre):
        return "Nombre con números"
    
    for letra in pais_nombre:
        if not (letra.isalpha() or 
                letra.isspace() or 
                letra == "-" or 
                letra == "(" or 
                letra == ")"):
            return "Nombre con caracteres inválidos"
    
    # Validar población (número entero positivo)
    if not pais_poblacion.lstrip("-").isdigit():
        return "Población no es número entero"
    
    if int(pais_poblacion) < 1:
        return "Población menor a 1"
    
    # Validar superficie (número entero no negativo)
    if not pais_superficie.lstrip("-").isdigit():
        return "Superficie no es número entero"
    
    if int(pais_superficie) < 0:
        return "Superficie menor a 0"
    
    # Validar campo ONU
    if pais_onu not in ["true", "false"]:
        return "Campo ONU inválido"
    
    return True