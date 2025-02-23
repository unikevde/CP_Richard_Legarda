import random
import json
import pickle
import numpy as np
import os
import nltk
from nltk.stem import WordNetLemmatizer
from keras.api.models import load_model

# Desactivar optimizaciones de oneDNN
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
lemmatizer = WordNetLemmatizer()

# Importamos los archivos generados en el código anterior
#intents = json.loads(open('intents.json', encoding='utf-8').read())
intents = json.loads(open('Web/intents.json', encoding='utf-8').read())
words = pickle.load(open('Web/words.pkl', 'rb'))
classes = pickle.load(open('Web/classes.pkl', 'rb'))
print("Contenido de classes:", classes)
print("Número de intenciones:", len(classes))
model = load_model('Web/chatbot_model.h5')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Función para limpiar la oración
def clean_up_sentence(sentence):
    sentence = sentence.lower()  # Convertir a minúsculas
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Convertir información en una bolsa de palabras
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predecir la clase de la oración
# Modificacion 11/12/2024 funcion:get_response quitada
def predecir_intencion(frase):
    bow = bag_of_words(frase)
    resultado = model.predict(np.array([bow]))[0]
    print("Probabilidades:", dict(zip(classes, resultado)))
    umbral = 0.20  # Umbral de confianza
    if max(resultado) < umbral:
        return None
    max_index = np.argmax(resultado)
    return classes[max_index]

# Obtener una respuesta basada en la categoría
def obtener_respuesta(tag, intents_json):
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i["tag"] == tag:
            return random.choice(i['responses'])
    return "No entiendo tu mensaje."
