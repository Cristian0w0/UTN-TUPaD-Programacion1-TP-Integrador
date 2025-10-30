#AGREGAR VALIDACION PARA PAISES CON MENOR O MAYOR CANTIDAD DE CAMPOS

import main
import csv

def cargar_pais(configuracion):
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
                next(lector, None)  # Saltar cabecera
                for fila in lector:
                    if fila and len(fila) > 0:
                        nombre_pais_cargado = fila[0].strip().capitalize()
                        paises_ya_cargados.add(nombre_pais_cargado)
        except FileNotFoundError:
            # Si el archivo no existe, empezar con conjunto vacío
            pass

        if nombre_pais.capitalize() in paises_ya_cargados:
            print(f"\nEl país {nombre_pais} ya está cargado.")
            continue

        # Buscar el país en los archivos de continentes
        print(f"\nBuscando {nombre_pais} en continentes...")
        
        path_africa = configuracion["Continentes"]["Africa"]
        path_asia = configuracion["Continentes"]["Asia"]
        path_europa = configuracion["Continentes"]["Europa"]
        path_america = configuracion["Continentes"]["America"]
        path_oceania = configuracion["Continentes"]["Oceania"]
        
        continentes_rutas = {
            "África": path_africa,
            "Asia": path_asia,
            "Europa": path_europa,
            "América": path_america,
            "Oceanía": path_oceania
        }

        pais_encontrado = None
        continente_encontrado = None

        # Buscar en todos los continentes
        for continente, ruta in continentes_rutas.items():
            try:
                with open(ruta, "r", encoding=codificacion, newline="") as archivo:
                    lector = csv.reader(archivo)
                    next(lector, None)  # Saltar cabecera
                    
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
    while True:
        print("\n--- Cargar paises por Continente ---\n"
        "1. Cargar África\n"
        "2. Cargar Asia\n"
        "3. Cargar Europa\n"
        "4. Cargar América\n"
        "5. Cargar Oceanía\n"
        "0. Volver al menú cargar")
        opcion = main.ingresar_opcion(rango_max=5)
        path_continente = ""
        match opcion:
            case 0:
                break
            case 1:
                path_continente = configuracion["Continentes"]["Africa"]
            case 2:
                path_continente = configuracion["Continentes"]["Asia"]
            case 3:
                path_continente = configuracion["Continentes"]["Europa"]
            case 4:
                path_continente = configuracion["Continentes"]["America"]
            case 5:
                path_continente = configuracion["Continentes"]["Oceania"]
            case _:
                continue
        
        path_paises_cargados = configuracion["Paises"]["Paises_Cargados"]
        codificacion = configuracion["Configuracion"]["codificacion"]
        nombre_continente = path_continente.split("\\")[-1].split(".")[0].capitalize()
        print(f"\nCargando países de {nombre_continente}")

        # Cargar todos los países existentes en paises_cargados
        paises_ya_cargados = set()
        try:
            with open(path_paises_cargados, "r", encoding=codificacion, newline="") as archivo:
                lector = csv.reader(archivo)
                next(lector, None)  # Saltar cabecera
                for fila in lector:
                    if fila and len(fila) > 0:
                        nombre_pais = fila[0].strip().capitalize()
                        paises_ya_cargados.add(nombre_pais)
        except FileNotFoundError:
            # Si el archivo no existe, empezar con conjunto vacío
            pass

        # Procesar países del continente
        with open(path_continente, "r", encoding=codificacion, newline="") as continente_archivo, \
            open(path_paises_cargados, "a", encoding=codificacion, newline="") as paises_archivo:
            
            lector_paises_entrantes = csv.reader(continente_archivo)
            next(lector_paises_entrantes)  # Saltar la cabecera

            paises_cargados_count = 0
            paises_duplicados_count = 0

            for pais_entrante in lector_paises_entrantes:
                if not pais_entrante:  # Saltar filas vacías
                    continue
                    
                pais_entrante_nombre = main.get_atributo(pais_entrante, 0).capitalize()
                
                if pais_entrante_nombre in paises_ya_cargados:
                    print(f"\n\tEl país {pais_entrante_nombre} ya está cargado, saltando...")
                    paises_duplicados_count += 1
                else:
                    # Escribir el país
                    paises_archivo.write("\n" + ",".join(pais_entrante))
                    # Agregar al conjunto para evitar duplicados en esta ejecución
                    paises_ya_cargados.add(pais_entrante_nombre)
                    print(f"\n\tPaís {pais_entrante_nombre} cargado correctamente.")
                    paises_cargados_count += 1

            print(f"\nResumen de carga:")
            print(f"\t- Países nuevos cargados: {paises_cargados_count}")
            print(f"\t- Países duplicados omitidos: {paises_duplicados_count}")



def cargar_onu(configuracion, estado_onu):
    
    #Carga todos los países de todos los continentes segun su campo onu.
    
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
    
    print(f"\n--- Cargando países {estado_texto} ---")

    # Cargar todos los países ya existentes en paises_cargados
    paises_ya_cargados = set()
    try:
        with open(path_cargados, "r", encoding=codificacion, newline="") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)  # Saltar cabecera
            for fila in lector:
                if fila and len(fila) > 0:
                    nombre_pais = fila[0].strip().capitalize()
                    paises_ya_cargados.add(nombre_pais)
    except FileNotFoundError:
        # Si el archivo no existe, empezar con conjunto vacío
        pass

    # Buscar países en todos los continentes que coincidan con el estado ONU
    path_africa = configuracion["Continentes"]["Africa"]
    path_asia = configuracion["Continentes"]["Asia"]
    path_europa = configuracion["Continentes"]["Europa"]
    path_america = configuracion["Continentes"]["America"]
    path_oceania = configuracion["Continentes"]["Oceania"]
    
    continentes_rutas = {
        "África": path_africa,
        "Asia": path_asia,
        "Europa": path_europa,
        "América": path_america,
        "Oceanía": path_oceania
    }

    paises_para_cargar = []
    paises_encontrados_por_continente = {}

    # Buscar en todos los continentes
    for continente, ruta in continentes_rutas.items():
        try:
            with open(ruta, "r", encoding=codificacion, newline="") as archivo:
                lector = csv.reader(archivo)
                next(lector, None)  # Saltar cabecera
                
                for fila in lector:
                    if fila and len(fila) >= 5:  # Asegurar que tiene campo ONU
                        nombre_pais = fila[0].strip().capitalize()
                        pais_onu = fila[4].strip().lower() if len(fila) > 4 else ""
                        
                        # Verificar si coincide con el estado ONU buscado y no está ya cargado
                        if pais_onu == estado_onu and nombre_pais not in paises_ya_cargados:
                            paises_para_cargar.append(fila)
                            if continente not in paises_encontrados_por_continente:
                                paises_encontrados_por_continente[continente] = 0
                            paises_encontrados_por_continente[continente] += 1
                            
        except FileNotFoundError:
            print(f"\nArchivo de {continente} no encontrado, saltando...")
            continue

    # Cargar los países encontrados
    if paises_para_cargar:
        with open(path_cargados, "a", encoding=codificacion, newline="") as archivo:
            for pais in paises_para_cargar:
                archivo.write("\n" + ",".join(pais))
        
        print(f"\nCarga completada:")
        print(f"Total de países {estado_texto} cargados: {len(paises_para_cargar)}")
        for continente, cantidad in paises_encontrados_por_continente.items():
            print(f"\t- {continente}: {cantidad} países")
    else:
        print(f"\nNo se encontraron países {estado_texto} nuevos para cargar.")



def limpiar_cargados(configuracion):
    #Limpia el archivo paises_cargados.csv, dejando solo la cabecera

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
        # Leer la cabecera del archivo actual
        with open(path_cargados, "r", encoding=codificacion, newline="") as archivo:
            lector = csv.reader(archivo)
            cabecera = next(lector, None)
        
        # Si el archivo existe y tiene cabecera, limpiarlo conservando la cabecera
        if cabecera:
            with open(path_cargados, "w", encoding=codificacion, newline="") as archivo:
                archivo.write(",".join(cabecera))
            print("\nSe limpiaron los paises cargados.")
        else:
            # Si no tiene cabecera, crear el archivo con cabecera por defecto
            with open(path_cargados, "w", encoding=codificacion, newline="") as archivo:
                cabecera_default = main.HEADER
                archivo.write(",".join(cabecera_default))
            print("\nArchivo para paises cargados creado con cabecera por defecto.")
            
    except FileNotFoundError:
        # Si el archivo no existe, crearlo con cabecera por defecto
        with open(path_cargados, "w", encoding=codificacion, newline="") as archivo:
            cabecera_default = main.HEADER
            archivo.write(",".join(cabecera_default))
        print("\nArchivo paises_cargados creado (no existía previamente).")
    
    except Exception as e:
        print(f"\nError al limpiar el archivo: {e}")



def limpiar_y_extraer(configuracion):
    while True:
        print("\n--- Extraer y limpiar países ---\n"
        "Este proceso validará y extraerá los países del archivo de 'países sin extraer', limpiando todos los otros archivos de datos.")
        confirmar = main.ingresar_opcion("\n¿Seguro que desea continuar? (1: Sí, 0: No): ", rango_max=1)
        if confirmar == 1:
            break
        elif confirmar == 0:
            return

    path_sin_extraer = configuracion["Paises"]["Paises_Sin_Extraer"]
    path_cargados = configuracion["Paises"]["Paises_Cargados"]
    path_africa = configuracion["Continentes"]["Africa"]
    path_asia = configuracion["Continentes"]["Asia"]
    path_europa = configuracion["Continentes"]["Europa"]
    path_america = configuracion["Continentes"]["America"]
    path_oceania = configuracion["Continentes"]["Oceania"]
    path_temporal = configuracion["Paises"]["temporal"]
    codificacion = configuracion["Configuracion"]["codificacion"]

    # Cargar países existentes en continentes para evitar duplicados
    paises_existentes = {}
    continentes_dict = {
        "África": path_africa,
        "Asia": path_asia,
        "Europa": path_europa,
        "América": path_america,
        "Oceanía": path_oceania
    }
    
    # Leer la cabecera del archivo sin_extraer para usarla en todos los archivos
    with open(path_sin_extraer, "r", encoding=codificacion, newline="") as sin_extraer_archivo:
        contenido_sin_extraer = csv.reader(sin_extraer_archivo)
        cabecera = next(contenido_sin_extraer)
    
    # Inicializar archivos de continentes con cabecera si están vacíos o no existen
    for continente_nombre, path_continente in continentes_dict.items():
        paises_existentes[continente_nombre] = set()
        try:
            # Verificar si el archivo existe y tiene contenido
            with open(path_continente, "r", encoding=codificacion, newline="") as continente_archivo:
                lector_continente = csv.reader(continente_archivo)
                primera_linea = next(lector_continente, None)
                if primera_linea:
                    # El archivo ya tiene cabecera, leer países existentes
                    for pais in lector_continente:
                        if pais and len(pais) > 0:
                            pais_nombre = main.get_atributo(pais, 0)
                            paises_existentes[continente_nombre].add(pais_nombre)
                else:
                    # Archivo existe pero está vacío, escribir cabecera
                    with open(path_continente, "w", encoding=codificacion, newline="") as continente_archivo:
                        continente_archivo.write(",".join(cabecera))
        except FileNotFoundError:
            # El archivo no existe, crearlo con cabecera
            with open(path_continente, "w", encoding=codificacion, newline="") as continente_archivo:
                continente_archivo.write(",".join(cabecera))
        except StopIteration:
            # Archivo existe pero está vacío, escribir cabecera
            with open(path_continente, "w", encoding=codificacion, newline="") as continente_archivo:
                continente_archivo.write(",".join(cabecera))

    # Procesar países sin extraer
    with open(path_sin_extraer, "r", encoding=codificacion, newline="") as sin_extraer_archivo, \
        open(path_cargados, "w", encoding=codificacion, newline="") as cargados_archivo, \
        open(path_temporal, "w", encoding=codificacion, newline="") as temporal_archivo:
        
        contenido_sin_extraer = csv.reader(sin_extraer_archivo)
        cabecera = next(contenido_sin_extraer)  # Leer cabecera otra vez
        indice_nombre = cabecera.index("nombre")
        indice_poblacion = cabecera.index("población")
        indice_superficie = cabecera.index("superficie")
        indice_continente = cabecera.index("continente")
        indice_onu = cabecera.index("onu")

        # Escribir cabecera en paises cargados y temporal
        cargados_archivo.write(",".join(cabecera))
        temporal_archivo.write(",".join(cabecera))

        # Listas para almacenar países procesados
        paises_para_continentes = {continente: [] for continente in continentes_dict.keys()}
        paises_para_temporal = []

        for pais in contenido_sin_extraer:
            pais_nombre = pais[indice_nombre].capitalize()
            pais_poblacion = pais[indice_poblacion]
            pais_superficie = pais[indice_superficie]
            pais_continente = pais[indice_continente].capitalize()
            pais_onu = pais[indice_onu].lower()

            campos_pais = [pais_nombre, pais_poblacion, pais_superficie, pais_continente, pais_onu]
            
            # Validar país
            valido_o_error = validar_pais(campos_pais, paises_existentes)
            if valido_o_error == True:
                # País válido - agregar a continente
                if pais_continente in paises_para_continentes:
                    paises_para_continentes[pais_continente].append(campos_pais)
                    # Actualizar conjunto de existentes para evitar duplicados en esta ejecución
                    paises_existentes[pais_continente].add(pais_nombre)
                    print(f"\n País {pais_nombre} validado correctamente, extrayendo a {pais_continente}...")
            elif isinstance(valido_o_error, str):
                # País inválido - agregar a temporal
                paises_para_temporal.append(campos_pais)
                print(f"\n País {pais_nombre} inválido ({valido_o_error}), saltar país...")

        # Escribir países inválidos en temporal
        for pais in paises_para_temporal:
            temporal_archivo.write("\n" + ",".join(pais))

    # Escribir países válidos en sus archivos de continente (modo append)
    for continente_nombre, paises in paises_para_continentes.items():
        if paises:  # Solo si hay países para este continente
            with open(continentes_dict[continente_nombre], "a", encoding=codificacion, newline="") as continente_archivo:
                for pais in paises:
                    continente_archivo.write("\n" + ",".join(pais))

    # Reemplazar paises_sin_extraer con temporal y limpiar temporal
    with open(path_sin_extraer, "w", encoding=codificacion, newline="") as sin_extraer_archivo, \
        open(path_temporal, "r+", encoding=codificacion, newline="") as temporal_archivo:
        
        # Copiar todo el contenido del temporal al sin_extraer
        contenido_temporal = temporal_archivo.read()
        sin_extraer_archivo.write(contenido_temporal)
        
        # Limpiar temporal (dejar solo cabecera)
        temporal_archivo.seek(0)
        temporal_archivo.truncate(0)
        temporal_archivo.write(",".join(cabecera))

    print(f"\n Proceso completado:")
    for continente_nombre, paises in paises_para_continentes.items():
        print(f"\t- {continente_nombre}: {len(paises)} países")
    print(f"\t- Países inválidos: {len(paises_para_temporal)}")



def validar_pais(campos_pais: list, paises_existentes: dict):
    #Función para validar un país segun sus campos
    
    # Validar cantidad de campos para evitar errores de índice
    if len(campos_pais) != 5:
        return f"Cantidad de campos incorrecta. Esperados: 5, Encontrados: {len(campos_pais)}"
    
    pais_nombre = campos_pais[0]
    pais_poblacion = campos_pais[1]
    pais_superficie = campos_pais[2]
    pais_continente = campos_pais[3]
    pais_onu = campos_pais[4]
    
    if "" in campos_pais:
        return "Al menos un campo obligatorio vacío"
    
    if pais_continente not in paises_existentes:
        return f"Continente '{pais_continente}' no válido"
    
    if pais_nombre in paises_existentes[pais_continente]:
        return f"País '{pais_nombre}' ya existe en {pais_continente}"
    
    if any(not (letra.isalpha() or letra.isspace()) for letra in pais_nombre):
        return "Nombre con números o caracteres especiales"
    
    if not pais_poblacion.lstrip("-").isdigit():
        return "Población no es número entero"
    
    if int(pais_poblacion) < 1:
        return "Población menor a 1"
    
    if not pais_superficie.lstrip("-").isdigit():
        return "Superficie no es número entero"
    
    if int(pais_superficie) < 0:
        return "Superficie menor a 0"
    
    if pais_onu not in ["true", "false"]:
        return "Campo ONU inválido"
    
    return True