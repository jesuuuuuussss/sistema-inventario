# Uso del Sistema de Inventario

El sistema registra y consulta productos en una interfaz web. Para la práctica se ejecuta en una red privada o se accede en local mediante un túnel SSH.

## Requisitos y arranque

Usa Python 3.11 o posterior con SQLite, incluido en la biblioteca estándar de Python. El usuario que inicia el programa necesita permiso de escritura en la carpeta de la base de datos.

Extrae el ZIP de GitHub Releases. Desde la raíz extraída ejecuta:

    python3 src/main.py --db datos/inventario.sqlite3

Abre http://127.0.0.1:8000. Registra un producto y consulta su código o parte de su nombre. Si el sistema se ejecuta en una máquina remota, establece un túnel con el usuario y puerto del servidor:

    ssh -L 8000:127.0.0.1:8000 -p 22 usuario@servidor

El archivo SQLite es independiente del programa. Define su ruta con --db para conservar el inventario al iniciar una versión diferente. En una base vacía puedes verificar alta y consulta con:

    python3 pruebas/verificar.py --version "$(cat VERSION)" --accion registrar

## Funciones del módulo

- Alta de productos con código único, precio en centavos MXN, cantidad entera y categoría.
- Consulta del inventario por código o nombre.
- Persistencia en SQLite.

## RELEASE y DEPLOY

El workflow de RELEASE prueba el código del commit y publica un ZIP con etiqueta y suma SHA-256. DEPLOY descarga ese archivo de la publicación, registra la suma y comprueba el arranque en el runner. En modo vm prepara una VM temporal Ubuntu, transfiere el ZIP por SCP y verifica la aplicación mediante SSH. Los ZIP quedan en ~/sistema-inventario/paquetes/ y las versiones extraídas en ~/sistema-inventario/versiones/.

Para ejecutar DEPLOY desde la pestaña Actions se selecciona la etiqueta y el destino. Usa runner para probar el paquete, vm para el ejercicio con una VM temporal o servidor para utilizar una máquina existente. Con anterior se indica una etiqueta publicada a la que regresar en el ejercicio. El parámetro filtro es la consulta esperada en la segunda versión.

El modo servidor usa DEPLOY_HOST, DEPLOY_USER, DEPLOY_KEY y DEPLOY_PORT como secretos. La variable DEPLOY_KNOWN_HOSTS almacena la línea pública de confianza del servidor. Esta máquina necesita Python 3.11 o posterior. La opción vm genera las llaves de la práctica durante la ejecución.
