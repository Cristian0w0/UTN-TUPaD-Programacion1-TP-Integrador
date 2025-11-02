import main, os

def mover_archivo(ruta_origen, ruta_destino):
    # Mover archivo de una ubicación a otra
    try:
        # Leer contenido del archivo original
        with open(ruta_origen, "rb") as archivo_origen:
            contenido = archivo_origen.read()
        
        # Escribir contenido en nueva ubicación
        with open(ruta_destino, "wb") as archivo_destino:
            archivo_destino.write(contenido)
        
        # Eliminar archivo original
        os.remove(ruta_origen)
        
        print(f"Archivo movido: {ruta_origen} -> {ruta_destino}")
        
    except Exception as e:
        print(f"Error al mover archivo {ruta_origen}: {e}")



def buscar_archivo(directorio, archivos_encontrados=None):
    # Buscar recursivamente archivos CSV en el directorio
    if archivos_encontrados is None:
        archivos_encontrados = {}
    
    try:
        # Recorrer todos los elementos del directorio
        for elemento in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, elemento)
            
            if os.path.isdir(ruta_completa):
                # Llamada recursiva para subdirectorios
                buscar_archivo(ruta_completa, archivos_encontrados)
            elif os.path.isfile(ruta_completa) and elemento.lower().endswith(".csv"):
                # Guardar archivo CSV encontrado
                archivos_encontrados[elemento.lower()] = ruta_completa
                
    except PermissionError:
        print(f"Sin permisos para acceder a: {directorio}")
    
    return archivos_encontrados



def organizar_archivos(configuracion):
    # Función principal para organizar archivos del sistema
    print("\nIniciando organización de archivos CSV...")
    
    directorio_base = os.getcwd()

    rutas_organizadas = {}
    
    # Obtener configuraciones del archivo de configuración
    path_paises_sin_extraer = configuracion["Paises"]["Paises_Sin_Extraer"]
    path_paises_cargados = configuracion["Paises"]["Paises_Cargados"]
    codificacion = configuracion["Configuracion"]["codificacion"]
    formato = configuracion["Configuracion"]["formato_archivos"]

    # Definir ubicaciones esperadas para cada archivo
    ubicaciones_esperadas = {
        "paises_sin_extraer.csv": os.path.join(directorio_base, path_paises_sin_extraer),
        "paises_cargados.csv": os.path.join(directorio_base, path_paises_cargados),
    }

    # Agregar continentes a las ubicaciones esperadas
    for continente in main.CONTINENTES:
        ubicaciones_esperadas[continente.lower() + "." + formato] = \
            os.path.join(directorio_base, configuracion["Continentes"][main.remover_tildes(continente)])
    
    # Buscar todos los archivos CSV en el directorio
    print("Buscando archivos CSV...")
    archivos_encontrados = buscar_archivo(directorio_base)
    
    # Procesar cada archivo esperado
    for archivo_esperado, ruta_destino in ubicaciones_esperadas.items():
        nombre_sin_extension = archivo_esperado.replace(".csv", "")
        
        if archivo_esperado in archivos_encontrados:
            # Archivo encontrado - mover si es necesario
            ruta_encontrada = archivos_encontrados[archivo_esperado]
            
            if ruta_encontrada != ruta_destino:
                # Crear directorio de destino si no existe
                directorio_destino = os.path.dirname(ruta_destino)
                if not os.path.exists(directorio_destino):
                    os.makedirs(directorio_destino)
                
                # Mover archivo a ubicación correcta
                mover_archivo(ruta_encontrada, ruta_destino)
            
            rutas_organizadas[nombre_sin_extension] = ruta_destino
            print(f"Procesado: {archivo_esperado}")
            
        else:
            # Archivo no encontrado - crear uno nuevo
            directorio_destino = os.path.dirname(ruta_destino)
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)
            
            try:
                # Crear archivo con cabecera por defecto
                with open(ruta_destino, "w", encoding=codificacion) as f:
                    f.writelines(",".join(main.HEADER))
                rutas_organizadas[nombre_sin_extension] = ruta_destino
                print(f"Creado: {ruta_destino}")
            except Exception as e:
                print(f"Error al crear {ruta_destino}: {e}")
    
    print("Organización completada!")
    return rutas_organizadas