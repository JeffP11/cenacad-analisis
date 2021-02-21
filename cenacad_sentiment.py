# coding=utf-8
# Colaboradores: Jeffrey Prado - Douglas Sabando
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def calculate_mean(array):
    """
        Calcula el promedio dado un arreglo con n elementos

            Argumentos:
                array (array) = arreglo con n elementos

            Salida:
                (int) = promedio 
    """
    suma = sum(array)
    total = len(array)
    return suma / total

def analyze_txt_textblob(sentences):
    """
        Realiza el análisis de sentimientos con TextBlob

            Argumentos:
                sentences (str) = comentarios del profesor
        
            Salida: 
                (int) = promedio de las polaridades en el comentario
    """
    textblob_polarity = []
    blob = TextBlob(sentences)
    for sentence in blob.sentences:
        textblob_polarity.append(round(sentence.sentiment.polarity, 2))
    mean = calculate_mean(textblob_polarity)
    return mean


def analyze_txt_vader(sentences, analyzer=analyzer):
    """
        Realiza el análisis de sentimientos con VADER
        
            Argumentos:
                sentences (str) = comentarios del profesor
                analyzer (SentimentIntensityAnalyzer()) = por defecto recibe la clase de Vader
                encargada de analizar los sentimientos
            
            Salida:
                (int) = promedio de las polaridades en el comentario
    """
    vader_polarity = []
    for sentence in sentences:
        scores = analyzer.polarity_scores(sentence)
        vader_polarity.append(round(scores['compound'], 2))
    mean = calculate_mean(vader_polarity)
    return mean
