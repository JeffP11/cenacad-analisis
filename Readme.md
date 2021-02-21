# Análisis de Sentimientos con TextBlob y VADER
Análisis cualitativo de los comentarios obtenidos en el censo académico de la Facultad de Ingeniería en Electricidad y Computación de la Escuela Superior Politécnica del Litoral en el período del 2015 1S al 2019 2S.
## Dependencias
Crear un ambiente virtual dentro del directorio con el *nombre* que desee [tener virtualenv instalado]

```
$ python -m pip install virtualenv
$ python -m venv <nombre>
```
Activar el ambiente virtual
```
Windows : $ <nombre>\Scripts\activate
Linux   : $ source <nombre>\bin\activate
```
Para desactivarlo:
```
$ deactivate
```
La consola de comandos debería reflejar:
```
(<nombre>) workspace-path>
```
Una vez que el ambiente virtual esté activado, instale las dependencias (requirements.txt)
```
$ python -m pip install -r requirements.txt
```
Finalmente, antes de proceder a  ejecutar el script principal, debe instalar dependencias de VADER con la librería NLTK. Desde dentro del entorno virtual ejecute first_script.py:

```
$ python first_script.py
```
que contiene lo siguiente, tranquilamente puede ejecutar las líneas en python.
```
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
```

## Instrucciones
Si no se cuenta con los directorios resultados y graficos llenos, entonces ejecutar script: cenacad-describe.py

## Colaboradores
```
Jeffrey Prado
Douglas Sabando
```