#ARCHIVO PY PARA CARGAR PAISES POR: 
    #PAISES POR NOMBRE
    #PAISES DE CONTINENTES ENTEROS
    #PAISES RECONOCIDOS POR LA ONU O NO RECONOCIDOS
#CAMBIAR NOMBRE A PAISES_SIN_EXTRAER Y BORRARLOS AL SER EXTRAIDOS
#CHECKEAR CAMPOS AL EXTRAER

import main
import csv

def cargar_pais():
    pass

def cargar_continente():
    while True:
        print("\n--- Cargar paises por Continente ---\n"
        "1. Cargar África\n"
        "2. Cargar Asia\n"
        "3. Cargar Europa\n"
        "4. Cargar América\n"
        "5. Cargar Oceanía\n"
        "0. Volver al menú cargar")
        opcion = main.ingresar_opcion(rango_max=5)
        

def cargar_onu(reconocido:bool):
    pass

def extraer(configuracion):

    path_paises_sin_cargar = configuracion["Paises"]["Paises_Sin_Cargar"]
    path_africa = configuracion["Continentes"]["Africa"]
    path_asia = configuracion["Continentes"]["Asia"]
    path_europa = configuracion["Continentes"]["Europa"]
    path_america = configuracion["Continentes"]["America"]
    path_oceania = configuracion["Continentes"]["Oceania"]
    codificacion = configuracion["Configuracion"]["codificacion"]

    with open(path_paises_sin_cargar, "r", encoding=codificacion, newline="") as paises_archivo, \
    open(path_africa, "w", encoding=codificacion, newline="") as africa_archivo, \
    open(path_asia, "w", encoding=codificacion, newline="") as asia_archivo, \
    open(path_europa, "w", encoding=codificacion, newline="") as europa_archivo, \
    open(path_america, "w", encoding=codificacion, newline="") as america_archivo, \
    open(path_oceania, "w", encoding=codificacion, newline="") as oceania_archivo:
        
        continentes_dict = {"África": africa_archivo, 
                            "Asia": asia_archivo, 
                            "Europa": europa_archivo, 
                            "América": america_archivo, 
                            "Oceanía": oceania_archivo}
        paises_contenido = csv.reader(paises_archivo)
        cabecera = next(paises_contenido)
        indice_continente = cabecera.index("continente")

        for campo_pais in cabecera:
            for continente_archivo in continentes_dict.values():
                continente_archivo.write(campo_pais)
                if campo_pais != "onu":
                    continente_archivo.write(",")

        for pais in paises_contenido:
            continente_nombre = pais[indice_continente].capitalize()
            if continente_nombre in continentes_dict.keys():
                continentes_dict[continente_nombre].write("\n")
                for campo_pais in pais:
                    continentes_dict[continente_nombre].write(campo_pais)
                    if (len(cabecera)-1 != pais.index(campo_pais)):
                        continentes_dict[continente_nombre].write(",")