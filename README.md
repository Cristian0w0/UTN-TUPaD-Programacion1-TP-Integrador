## UTN - TP Integrador: Gestor de países (CSV)

Breve introducción
-------------------
Este proyecto es un programa en Python que gestiona datos de países almacenados en archivos CSV. Permite:
- Organizar archivos CSV del proyecto (mover/crear archivos esperados).
- Extraer y validar países desde un archivo maestro (`paises_sin_extraer.csv`) hacia archivos por continente.
- Cargar países a un archivo de "paises_cargados.csv" desde diferentes orígenes (por nombre, por continente, por estado ONU).
- Filtrar, ordenar y mostrar estadísticas sobre los países cargados.

Requisitos
----------
- Python 3.8+ (probado en entornos Windows). 
- Codificación recomendada: `utf-8-sig` (el proyecto usa esta codificación en `configuracion.ini`).

Estructura del repositorio
--------------------------
- `main.py` — Punto de entrada. Menús interactivos y funciones auxiliares.
- `configuracion.ini` — Rutas esperadas para los archivos CSV y configuración (formato, codificación).
- `paises_sin_extraer.csv` — Archivo maestro con todos los países por procesar (incluye países no reconocidos por la ONU).
- `scripts/` — Contiene los módulos que implementan la lógica:
  - `organizar.py` — Busca archivos CSV en el árbol, los mueve a las rutas esperadas o crea archivos nuevos con cabecera por defecto.
  - `cargar.py` — Funciones para cargar países (por nombre, por continente, por estado ONU), introducir manualmente, limpiar y extraer.
  - `filtrar.py` — Funciones para filtrar países por continente, población o superficie.
  - `ordenar.py` — Ordena el archivo de `paises_cargados.csv` por nombre, población o superficie (asc/desc) y lo sobreescribe.
  - `mostrar.py` — Muestra estadísticas: mayor/menor población, promedios, conteo por continente y listado de cargados.

Formato de los CSV
------------------
Todos los CSV usan la misma cabecera y columnas (orden esperado):

nombre,población,superficie,continente,onu

- `nombre` — Nombre del país (texto).
- `población` — Entero (sin separadores de miles).
- `superficie` — Entero (km^2).
- `continente` — Nombre del continente tal como se lista en `main.CONTINENTES` (p. ej. "América", "Europa").
- `onu` — "true" o "false" según reconocimiento por la ONU.

Configuración (`configuracion.ini`)
----------------------------------
El archivo `configuracion.ini` define:
- Rutas relativas de: `Paises_Sin_Extraer`, `Paises_Cargados`.
- Rutas a archivos por continente dentro de la sección `[Continentes]`.
- Formato de archivos (`formato_archivos`) y `codificacion` (por defecto `utf-8-sig`).

Cómo ejecutar
--------------
Ejecutar comando `main.py`:

python .\main.py

El programa arranca ejecutando la función `organizar.organizar_archivos` y luego muestra un menú interactivo en consola con opciones para filtrar, ordenar, mostrar y cargar países.

Uso rápido (menu principal)
---------------------------
- 1. Filtrar países — abre submenú para filtrar por continente, población o superficie.
- 2. Ordenar países — ordenar el archivo `paises_cargados.csv` por nombre/población/superficie.
- 3. Mostrar estadísticas — mayor/menor población, promedios, conteo por continente, ver países cargados.
- 4. Cargar países — submenú para cargar por nombre, cargar todo un continente, cargar por estado ONU, introducir manualmente, limpiar cargados o proceso "Limpiar todo y Extraer".

Notas y supuestos
------------------
- El programa espera rutas relativas definidas en `configuracion.ini`. Si los archivos no existen, `organizar.py` intentará crearlos (con la cabecera por defecto).
- Codificación: use `utf-8-sig` para evitar problemas con BOM en CSVs; esto ya está configurado por defecto.
- Al introducir valores numéricos, el programa asume enteros válidos y realiza conversiones directas (puede lanzar excepciones si los datos de los CSV no son íntegros).
- Algunos nombres y comparaciones usan `.capitalize()` y normalización de tildes en las claves de las rutas; hay que ingresar los nombres tal como el CSV los tiene o con capitalización estándar para encontrarlos.

— Fin —