# Magister-Reto
## Requisitos
Para el funcionamiento correcto del programa, es necesario instalar los siguientes módulos de Python:
- Flask
- SQLAlchemy
- BeautifulSoup
- Geopy
- Selenium
- Requests

Para ello, será necesario ejecutar en la terminal los siguientes comandos:
### En Linux
- sudo pip3 install flask
- sudo pip3 install flask-sqlalchemy
- sudo pip3 install beautifulsoup4
- sudo pip3 install geopy
- sudo pip3 install selenium
- sudo pip3 install geopy
- sudo pip3 install requests

### En Windows
- python3 -mpip install flask
- python3 -mpip install flask-sqlalchemy
- python3 -mpip install beautifulsoup4
- python3 -mpip install geopy
- python3 -mpip install selenium
- python3 -mpip install geopy
- python3 -mpip install requests

Asimismo, es necesario instalar geckodriver y el navegador Firefox para el funcionamiento del módulo Selenium. Descarga la herramienta a partir de este enlace: https://github.com/mozilla/geckodriver/releases
Una vez descargado, es lo siguiente es descomprimir el paquete y ubicarlo en un directorio. Para la detección de geckodriver, es necesario cambiar el directorio en la línea 14 de reto.py:

- driver = webdriver.Firefox(firefox_options=options, executable_path = 'C:/Users/Javier/Downloads/geckodriver.exe')

En esa línea de código, es necesario cambiar la variable "executable_path" por la ruta donde se encuentre geckodriver.exe

A continuación se crea la base de datos. El usuario utilizado para la realización de la prueba se denomina "postgres", y la contraseña es "password". Esta información es importante, debido a que el script de Python accede a la base de datos a través de este usuario. Para ello, desde pgAdmin 4, una vez introducidas las credenciales, selecciona CREATE, y a continuación DATABASE. En el nombre de la base de datos escribe "colegios" y a continuación pulsa Save. Una vez creada la base de datos, accede a ella y pulsando el botón derecho selecciona Query Tool. En la barra superior se sitúa la opción de abrir el archivo. Al seleccionar la opción pulsa sobre el archivo script.sql incluído en el repositorio. Una vez cargado el fichero, pulsa sobre el botón de play para ejecutar el script e incluir el esquema relacional de la base de datos. Por último, solo es necesario ejecutar el script de Python a través de la terminal usando:
- python3 reto.py

## Funcionamiento
Para la realización de la búsqueda de Web Scraping, primero se ha comprobado el funcionamiento de la página web. Al realizar una búsqueda, el formato de las direcciones URL era la siguiente:
- https://www.scholarum.es/es/buscador-centros/"PROVINCIA"/"CENTRO"%7C"CENTRO"/"LATITUD"/"LONGITUD"/"DISTANCIA"

Por ello, a través del módulo geopy es posible obtener la latitud, longitud y la dirección exacta, incluyendo la provincia del string escrito en el formulario. A través del formulario se almacenan las queries en la base de datos. En caso de que no haya ninguna query, no será posible ejecutar la funcionalidad de web scraping, ya que no aparecerá el botón. Cuando existen queries pendientes, al pulsar sobre el scraper, se ejecuta la primera query. Tras unos segundos de recopilación de datos, aprovechando los módulos de BeautifulSoup y Selenium se muestran por pantalla los resultados y se almacenan en la tabla "schools".