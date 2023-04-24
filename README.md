### Clasificador de lenguaje ofensivo para mensajes de texto en español

#### Resumen de funcionalidad :computer:

Primero, se importan varias librerías, como NLTK y Scikit-Learn, y se cargan dos listas de palabras ofensivas y no ofensivas en español a partir de archivos CSV. A continuación, se unen ambas listas en una sola lista de tuplas (palabra, etiqueta), que se mezcla aleatoriamente y se divide en conjuntos de entrenamiento y prueba.

Se define una función para extraer características de las palabras y se entrena un clasificador Naive Bayes (puedes ocupar los démas comentados en el código) con el conjunto de entrenamiento. Se evalúa la precisión del clasificador con el conjunto de prueba.

Luego, se crea una función para procesar los mensajes del bot de Telegram, que elimina los caracteres especiales y números, tokeniza el mensaje en palabras y verifica si alguna palabra es ofensiva utilizando el clasificador entrenado. Si el mensaje contiene una palabra ofensiva, se elimina el mensaje y se envía una notificación al usuario que lo envió.

Finalmente, se crea un objeto Updater con el token del bot de Telegram, se agrega el MessageHandler al dispatcher y se inicia el bot. El bot se mantiene en ejecución hasta que se detiene manualmente.

#### Ejecución de código ⚙️

1. Realizar un entorno virtual. En este caso se hace uso de pipenv.
    - <code>pipenv shell</code>
2. Instalar las librerias necesarias.
    - <code>pipenv install -r requirements.txt</code>
3. Introducir su token en la linea de código correspondiente del bot creado en telegram.    
4. Ejecutar el archivo python.
    - <code>pipenv run py detector.py</code>

#### Construido con 🛠️

* [Python](https://www.python.org/) - Lenguaje de programación
* [NLTK](https://www.nltk.org/) - Libreria NLTK
* [Telegram Bot](https://python-telegram-bot.org/) - Libreria Telegram
* [Sklearn](https://scikit-learn.org/stable/) - Libreria Scikit-Learn

#### Autor ✒️

* **Víctor García** [vicogarcia16](https://github.com/vicogarcia16) 
