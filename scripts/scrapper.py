import csv

CONTINENTES = ["África", "Asia", "Europa", "América", "Oceanía"]

def scrap_continente(continente):
    continente_formateado = continente.lower()
    with open("paises.csv", "r", encoding="utf-8-sig", newline="") as paises_archivo:
        with open(continente_formateado + ".csv", "w", encoding="utf-8-sig", newline="") as continente_archivo:
            paises_contenido = csv.reader(paises_archivo)
            cabecera = next(paises_contenido)
            indice_continente = cabecera.index("continente")
            for campo_pais in cabecera:
                continente_archivo.write(campo_pais)
                if campo_pais != "onu":
                    continente_archivo.write(",")
            for pais in paises_contenido:
                if (pais[indice_continente].lower() == continente_formateado):
                    continente_archivo.write("\n")
                    for campo_pais in pais:
                        continente_archivo.write(campo_pais)
                        if (len(cabecera)-1 != pais.index(campo_pais)):
                            continente_archivo.write(",")

#for continente in CONTINENTES:
#    scrap_continente(continente)

def scrap(configuracion):

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
        
        continentes_dict = {"África": africa_archivo, "Asia": asia_archivo, "Europa": europa_archivo, "América": america_archivo, "Oceanía": oceania_archivo}
        paises_contenido = csv.reader(paises_archivo)
        cabecera = next(paises_contenido)
        indice_continente = cabecera.index("continente")

        for campo_pais in cabecera:
            for continente in continentes_dict:
                continente.write(campo_pais)
                if campo_pais != "onu":
                    continente.write(",")

        for pais in paises_contenido:
            continente = pais[indice_continente].capitalize()
            if (continente in continentes_dict):
                continentes_dict[continente].write("\n")
                for campo_pais in pais:
                    continente.write(campo_pais)
                    if (len(cabecera)-1 != pais.index(campo_pais)):
                        continente.write(",")

scrap()