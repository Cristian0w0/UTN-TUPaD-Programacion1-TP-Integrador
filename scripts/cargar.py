#ARCHIVO PY PARA CARGAR PAISES POR: 
    #*PAISES POR NOMBRE
    #*PAISES DE CONTINENTES ENTEROS
    #*PAISES RECONOCIDOS POR LA ONU O NO RECONOCIDOS

import main

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