def analysis():
    text = "Texblob es buena. VADER se dedica a analisis de sentimientos."

    blob = TextBlob(text)

    if (blob.detect_language() != 'en'):
        blob = blob.translate(from_lang = 'es', to='en')

    blob.tags
    print(blob.tags)

    blob.noun_phrases
    print(blob.noun_phrases)

    for sentence in blob.sentences:
        # polarity      ->  -1 a 1  ->  sentimientos negativos a positivos
        # subjectivity  ->   0 a 1  ->  0 es objetivo y 1 subjetivo
        print(f""" \n{sentence}
        polarity\t-> {round(sentence.sentiment.polarity,2)}
        subjectivity\t-> {round(sentence.sentiment.subjectivity,2)}""")


if __name__ == "__main__":
    from textblob import TextBlob
    # from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analysis();
