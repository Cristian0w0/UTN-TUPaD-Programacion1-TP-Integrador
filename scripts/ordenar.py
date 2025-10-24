import csv

def asc_desc(campo:str):
    while True:
        opcion = input("\nOrdenar de forma Ascendente o Descendente? (A/D) (0 " \
        "para volver al menú anterior): ").upper()
        if (opcion in ["A", "D"]):
            break
        elif (opcion == "0"):
            return
        else:
            print("Opción inválida")
    with open("paises.csv", "r", encoding="utf-8-sig", newline="") as archivo:
        contenido = csv.reader(archivo)
        header = next(contenido)
        print(f"\n--- Paises ordenados por {campo.capitalize()} de forma " \
        f"{"Ascendente" if opcion == "A" else "Descendente"} ---")
        orden = True if opcion == "D" else False
        if (campo in ("población", "superficie")):
            contenido_ordenado = sorted(contenido, key=lambda 
                                    x: int(x[header.index(campo)]), reverse=orden)
        else:
            contenido_ordenado = sorted(contenido, key=lambda 
                                    x: x[header.index(campo)], reverse=orden)
        for line in contenido_ordenado:
            print(line)