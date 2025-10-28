import os

def mover_archivo(ruta_origen, ruta_destino):
    """
    Función para mover un archivo.
    
    Args:
        ruta_origen (str): Ruta del archivo a mover
        ruta_destino (str): Ruta destino del archivo
    """
    try:
        # Leer el contenido del archivo origen
        with open(ruta_origen, 'rb') as archivo_origen:
            contenido = archivo_origen.read()
        
        # Escribir el contenido en el archivo destino
        with open(ruta_destino, 'wb') as archivo_destino:
            archivo_destino.write(contenido)
        
        # Eliminar el archivo origen
        os.remove(ruta_origen)
        
        print(f"✓ Archivo movido: {ruta_origen} -> {ruta_destino}")
        
    except Exception as e:
        print(f"✗ Error al mover archivo {ruta_origen}: {e}")

def buscar_archivo(directorio, archivos_encontrados=None):
    """
    Función para buscar archivos CSV recursivamente.
    
    Args:
        directorio (str): Directorio donde buscar
        archivos_encontrados (dict): Diccionario para almacenar archivos encontrados
    
    Returns:
        dict: Diccionario con archivos encontrados
    """
    if archivos_encontrados is None:
        archivos_encontrados = {}
    
    try:
        for elemento in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, elemento)
            
            if os.path.isdir(ruta_completa):
                # Llamada recursiva para directorios
                buscar_archivo(ruta_completa, archivos_encontrados)
            elif os.path.isfile(ruta_completa) and elemento.lower().endswith('.csv'):
                # Agregar archivo CSV al diccionario
                archivos_encontrados[elemento.lower()] = ruta_completa
                
    except PermissionError:
        print(f"Sin permisos para acceder a: {directorio}")
    
    return archivos_encontrados

def organizar_archivos(configuracion):
    """
    Función para organizar todos los archivos CSV.
    
    Args:
        directorio_base (str): Ruta base del proyecto
    
    Returns:
        dict: Diccionario con las rutas organizadas
    """
    print("Iniciando organización de archivos CSV...")
    
    directorio_base = os.getcwd()

    # Diccionario para almacenar las rutas finales
    rutas_organizadas = {}
    
    path_paises_sin_extraer = configuracion["Paises"]["Paises_Sin_Extraer"]
    path_paises_cargados = configuracion["Paises"]["Paises_Cargados"]
    path_africa = configuracion["Continentes"]["Africa"]
    path_asia = configuracion["Continentes"]["Asia"]
    path_europa = configuracion["Continentes"]["Europa"]
    path_america = configuracion["Continentes"]["America"]
    path_oceania = configuracion["Continentes"]["Oceania"]
    path_temporal = configuracion["Paises"]["Temporal"]

    # Ubicaciones esperadas
    ubicaciones_esperadas = {
        'áfrica.csv': os.path.join(directorio_base, path_africa),
        'asia.csv': os.path.join(directorio_base, path_asia),
        'europa.csv': os.path.join(directorio_base, path_europa),
        'américa.csv': os.path.join(directorio_base, path_america),
        'oceanía.csv': os.path.join(directorio_base, path_oceania),
        'paises_sin_extraer.csv': os.path.join(directorio_base, path_paises_sin_extraer),
        'paises_cargados.csv': os.path.join(directorio_base, path_paises_cargados),
        'temporal.csv': os.path.join(directorio_base, path_temporal)
    }
    
    # Buscar todos los archivos CSV recursivamente
    print("Buscando archivos CSV...")
    archivos_encontrados = buscar_archivo(directorio_base)
    
    # Procesar cada archivo esperado
    for archivo_esperado, ruta_destino in ubicaciones_esperadas.items():
        nombre_sin_extension = archivo_esperado.replace('.csv', '')
        
        # Verificar si el archivo fue encontrado
        if archivo_esperado in archivos_encontrados:
            ruta_encontrada = archivos_encontrados[archivo_esperado]
            
            # Si no está en la ubicación correcta, moverlo
            if ruta_encontrada != ruta_destino:
                # Crear directorio destino si no existe
                directorio_destino = os.path.dirname(ruta_destino)
                if not os.path.exists(directorio_destino):
                    os.makedirs(directorio_destino)
                
                # Mover el archivo usando solo os
                mover_archivo(ruta_encontrada, ruta_destino)
            
            rutas_organizadas[nombre_sin_extension] = ruta_destino
            print(f"✓ Procesado: {archivo_esperado}")
            
        else:
            # Crear archivo si no existe
            directorio_destino = os.path.dirname(ruta_destino)
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)
            
            try:
                with open(ruta_destino, 'w', encoding='utf-8') as f:
                    f.write('')  # Archivo CSV vacío
                rutas_organizadas[nombre_sin_extension] = ruta_destino
                print(f"✓ Creado: {ruta_destino}")
            except Exception as e:
                print(f"✗ Error al crear {ruta_destino}: {e}")
    
    print("✅ Organización completada!")
    return rutas_organizadas