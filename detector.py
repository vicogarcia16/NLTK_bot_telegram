import nltk
from nltk.classify import DecisionTreeClassifier, SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import csv
import os
import random
import re
import logging
from telegram.ext import Updater, MessageHandler, Filters

# Activar los logs de error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)

# Lista de palabras ofensivas en español
offensive_words = []
with open('data/palabras_obs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Obtener la palabra de la columna "palabra"
        palabra = row['palabra']
        # Agregar la palabra a una lista de palabras ofensivas
        offensive_words.append(palabra)

# Lista de palabras no ofensivas en español
non_offensive_words = []
with open('data/palabras_pos.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        palabra = row['palabra']
        # Agregar la palabra a una list
        non_offensive_words.append(palabra)
        
# Unir ambas listas y crear una lista de tuplas (palabra, etiqueta)
labeled_words = [(word, 'ofensivo') for word in offensive_words] + [(word, 'no ofensivo') for word in non_offensive_words]

# Mezclar aleatoriamente la lista de tuplas
random.shuffle(labeled_words)

# Dividir la lista en conjunto de entrenamiento (80%) y conjunto de prueba (20%)
train_set = labeled_words[:int(len(labeled_words) * 0.8)]
test_set = labeled_words[int(len(labeled_words) * 0.8):]

# Definir una función para extraer características de las palabras
def extract_features(word):
    return {
        'last_letter': word[-1],
        'last_two_letters': word[-2:]
    }
    

# Entrenar un clasificador con el conjunto de entrenamiento
classifier = nltk.NaiveBayesClassifier.train([(extract_features(word), label) for (word, label) in train_set])
# classifier = DecisionTreeClassifier.train([(extract_features(word), label) for (word, label) in train_set])
# classifier = SklearnClassifier(SVC()).train([(extract_features(word), label) for (word, label) in train_set])
# classifier = SklearnClassifier(LogisticRegression()).train([(extract_features(word), label) for (word, label) in train_set])

# Evaluar el rendimiento del clasificador con el conjunto de prueba
accuracy = nltk.classify.accuracy(classifier, [(extract_features(word), label) for (word, label) in test_set])
print('Precisión del clasificador:', accuracy)

# Crear una función para procesar los mensajes del bot de Telegram
def message_handler(update, context):
    # Obtener el mensaje
    message = update.message.text.lower()
    # Eliminar caracteres especiales y números
    message = re.sub(r'[^a-záéíóúñü ]', '', message)
    # Tokenizar el mensaje
    words = message.split()
    # Verificar si alguna palabra es ofensiva
    for word in words:
        if classifier.classify(extract_features(word)) == 'ofensivo':
            # Eliminar el mensaje
            update.message.delete()
            # Enviar una notificación al usuario que envió el mensaje
            context.bot.send_message(chat_id=update.message.chat_id, text='Tu mensaje ha sido eliminado por contener lenguaje ofensivo.')
            break

# Crear un objeto Updater con el token del bot de Telegram
updater = Updater(os.environ['TOKEN'])

# Obtener el dispatcher del Updater
dispatcher = updater.dispatcher

# Agregar el MessageHandler al dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))

# Iniciar el bot
updater.start_polling()

# Mantener al bot en ejecución
updater.idle()
