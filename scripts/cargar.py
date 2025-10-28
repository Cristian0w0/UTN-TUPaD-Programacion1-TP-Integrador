#ARCHIVO PY PARA CARGAR PAISES POR: 
    #PAISES POR NOMBRE
    #PAISES RECONOCIDOS POR LA ONU O NO RECONOCIDOS

import main
import csv

def cargar_pais():
    pass

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
        print(f"Cargando países de {nombre_continente}")

        with open(path_continente, "r", encoding=codificacion, newline="") as continente_archivo, \
        open(path_paises_cargados, "r+", encoding=codificacion, newline="") as paises_archivo:
            lector_paises_cargados = csv.reader(paises_archivo)
            lector_paises_entrantes = csv.reader(continente_archivo)
            next(lector_paises_entrantes)  # Saltar la cabecera

            for pais_entrante in lector_paises_entrantes:
                pais_entrante_nombre = main.get_atributo(pais_entrante, 0)
                pais_ya_cargado = False
                paises_archivo.seek(0)
                next(lector_paises_cargados)  # Saltar la cabecera
                for pais_cargado in lector_paises_cargados:
                    pais_cargado_nombre = main.get_atributo(pais_cargado, 0)
                    if pais_entrante_nombre == pais_cargado_nombre:
                        pais_ya_cargado = True
                        print(f"El país {pais_entrante_nombre} ya está cargado, saltando...")
                        break
                if not pais_ya_cargado:
                    paises_archivo.seek(0, 2)  # Mover al final del archivo para escribir
                    paises_archivo.write("\n" + ",".join(pais_entrante))
                    print(f"✓ País {pais_entrante_nombre} cargado correctamente.")

def cargar_onu(reconocido:bool):
    pass

def extraer(configuracion):

    path_sin_extraer = configuracion["Paises"]["Paises_Sin_Extraer"]
    path_cargados = configuracion["Paises"]["Paises_Cargados"]
    path_africa = configuracion["Continentes"]["Africa"]
    path_asia = configuracion["Continentes"]["Asia"]
    path_europa = configuracion["Continentes"]["Europa"]
    path_america = configuracion["Continentes"]["America"]
    path_oceania = configuracion["Continentes"]["Oceania"]
    path_temporal = configuracion["Paises"]["temporal"]
    codificacion = configuracion["Configuracion"]["codificacion"]

    with open(path_sin_extraer, "r", encoding=codificacion, newline="") as sin_extraer_archivo, \
    open(path_cargados, "w", encoding=codificacion, newline="") as cargados_archivo, \
    open(path_africa, "r+", encoding=codificacion, newline="") as africa_archivo, \
    open(path_asia, "r+", encoding=codificacion, newline="") as asia_archivo, \
    open(path_europa, "r+", encoding=codificacion, newline="") as europa_archivo, \
    open(path_america, "r+", encoding=codificacion, newline="") as america_archivo, \
    open(path_oceania, "r+", encoding=codificacion, newline="") as oceania_archivo, \
    open(path_temporal, "w", encoding=codificacion, newline="") as temporal_archivo:
        
        continentes_dict = {"África": africa_archivo, 
                            "Asia": asia_archivo, 
                            "Europa": europa_archivo, 
                            "América": america_archivo, 
                            "Oceanía": oceania_archivo}
        contenido_sin_extraer = csv.reader(sin_extraer_archivo)
        cabecera = next(contenido_sin_extraer)
        indice_nombre = cabecera.index("nombre")
        indice_poblacion = cabecera.index("población")
        indice_superficie = cabecera.index("superficie")
        indice_continente = cabecera.index("continente")
        indice_onu = cabecera.index("onu")

        print(cabecera)

        for continente_archivo in continentes_dict.values():
            continente_archivo.write(",".join(cabecera))
        cargados_archivo.write(",".join(cabecera))
        temporal_archivo.write(",".join(cabecera))

        for pais in contenido_sin_extraer:
            pais_nombre = pais[indice_nombre].capitalize()
            pais_poblacion = pais[indice_poblacion]
            pais_superficie = pais[indice_superficie]
            pais_continente = pais[indice_continente].capitalize()
            pais_onu = pais[indice_onu].lower()

            campos_pais = [pais_nombre, pais_poblacion, pais_superficie, pais_continente, pais_onu]
            
            extraer = False
            destino = temporal_archivo

            print(f"Procesando país: {pais}")

            while True:
                if "" in campos_pais:
                    print("Al menos un campo obligatorio vacío, saltar pais")
                    break
                if not pais_continente in continentes_dict.keys():
                    print("Continente no valido, saltar pais")
                    break
                if pais_continente in continentes_dict.keys():
                    if pais_existente(continentes_dict[pais_continente], pais_nombre):
                        print("País ya existe en el archivo, saltar país")
                        break
                if any(letra.isdigit() for letra in pais_nombre):
                    print("Nombre con numeros, saltar pais")
                    break
                if not pais_poblacion.lstrip("-").isdigit():
                    print("Poblacion no es numero entero positivo, saltar pais")
                    break
                if pais_poblacion.lstrip("-").isdigit and int(pais_poblacion) < 1:
                    print("Poblacion menor a 1, saltar pais")
                    break
                if not pais_superficie.lstrip("-").isdigit():
                    print("Superficie no es numero entero mayor o igual a 0, saltar pais")
                    break
                if pais_superficie.lstrip("-").isdigit() and int(pais_superficie) < 0:
                    print("Superficie menor a 0, saltar pais")
                    break
                if pais_onu not in ["true", "false"]:
                    print("Campo ONU invalido, saltar pais")
                    break
                print(f"Pais {pais_nombre} validado correctamente, extrayendo...")
                extraer = True
                break

            print("")

            if extraer:
                destino = continentes_dict[pais_continente]
            
            print("\n" + ",".join(campos_pais))
            destino.write("\n" + ",".join(campos_pais))

    with open(path_sin_extraer, "w", encoding=codificacion, newline="") as sin_extraer_archivo, \
    open(path_temporal, "r+", encoding=codificacion, newline="") as temporal_archivo:
        contenido_temporal = temporal_archivo.read()
        sin_extraer_archivo.write(contenido_temporal)
        temporal_archivo.seek(0)
        temporal_archivo.truncate(0)

def pais_existente(archivo, pais_nuevo_nombre):
    """Verifica si un país ya existe en el archivo"""
    posicion_actual = archivo.tell()
    archivo.seek(0)
    
    next(archivo)  # Saltar cabecera
    existe = False
    
    for linea in archivo:
        pais_guardado_nombre = main.get_atributo(linea, 0)
        if pais_nuevo_nombre == pais_guardado_nombre:
            existe = True
            break
    
    archivo.seek(posicion_actual)
    return existe