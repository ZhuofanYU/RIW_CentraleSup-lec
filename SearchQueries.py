import os
import nltk
import numpy as np
import math
import pickle as pkl
from tqdm import tqdm

Vocabulary = pkl.load(open("Vocabulary.pkl", "rb"))
Freq_Vocabulary = pkl.load(open("Freq_Vocabulary.pkl", "rb"))
Collection = pkl.load(open("Collection.pkl", "rb"))
Absolute_Values = pkl.load(open("Absolute_Values.pkl", "rb"))
TF_IDF = pkl.load(open("TF_IDF.pkl","rb"))

query = "stanford students"


def preprocess_query(query):

    processed_query = {}

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    stop_words = nltk.corpus.stopwords.words('english')
    lematizer = nltk.stem.WordNetLemmatizer()
    steamer = nltk.stem.PorterStemmer()

    query = tokenizer.tokenize(query)

    query_no_stop_words = []
    for word in query:
        if word not in stop_words:
            query_no_stop_words.append(word)

    query = query_no_stop_words
    query = [lematizer.lemmatize(word) for word in query]
    query = [steamer.stem(word) for word in query]

    for word in query:

        try:
            idf = math.log(len(Collection) / Freq_Vocabulary[word], 10)
            tf = query.count(word)
            processed_query[word] = tf*idf
        except KeyError:
            pass

    return processed_query


query = preprocess_query(query)

abs_query = 0.000001
for word in query:
    abs_query = abs_query + query[word]**2
abs_query = math.sqrt(abs_query)

Score = []
for document in Collection:

    dot_product = 0
    for word in query:
        try:
            dot_product = dot_product + TF_IDF[document, word]*query[word]
        except KeyError:
            pass

    angle = math.acos(dot_product/(Absolute_Values[document]*abs_query))
    Score.append((document, angle))

Query_Results = sorted(Score, key=lambda x: x[1])

i = 0
for results in Query_Results:

    if i == 10:
        break
    i = i + 1

    print(results[0], results[1])





