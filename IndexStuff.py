from Utils.Lab1 import *
import numpy as np
import math
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

query = "KENNEDY ADMINISTRATION PRESSURE ON NGO DINH DIEM TO STOP"
"""
    Start by opening the collection
"""
collection_TIME = loadData("./Data/Time/TIME.ALL")

pre_processed_collection_TIME = collection_lemmatize(remove_stop_words(tokenize_Regexp_corpus(collection_TIME),"./Data/Time/TIME.STP"))

# A completer

"""
    Store the list with the keys from the document collection
    O VALLEY OF PLENTLY!!!!!!
"""
document_ids = []
for key in pre_processed_collection_TIME:
    document_ids.append(key)

"""
    Get the vocabulary from the collection to construct the td_idf matrix!
"""
def get_vocabulary(collection):
    vocabulary = []

    for key in collection:
        for word in collection[key]:
            if word not in vocabulary:
                vocabulary.append(word)

    return vocabulary


def get_stats_document(document):
    stats = {}
    # A completer
    # First the maximal frequency
    freq_max = 0
    for word in document:
        n = document.count(word)
        if n >= freq_max:
            freq_max = n

    unique_terms = []
    for word in document:
        if word not in unique_terms:
            unique_terms.append(word)

    freq_moy = 0
    for word in document:
        freq_moy = freq_moy + document.count(word)
    freq_moy = freq_moy / len(document)

    stats["freq_max"] = freq_max
    stats["unique_terms"] = len(unique_terms)
    stats["freq_moy"] = freq_moy

    return stats


def get_stats_collection(collection):
    stats = {}
    stats["nb_docs"] = len(collection)
    for key in collection:
        stats[key] = get_stats_document(collection[key])

    return stats


Vocabulary = get_vocabulary(pre_processed_collection_TIME)
Stats = get_stats_collection(pre_processed_collection_TIME)

TD_IDF = np.zeros((len(pre_processed_collection_TIME),len(Vocabulary)))


for j,word in enumerate(Vocabulary):
    df = 0
    for i,key in enumerate(pre_processed_collection_TIME):
        if word in pre_processed_collection_TIME[key]:
            df = df + 1

    idf = math.log(len(pre_processed_collection_TIME) / df, 10)

    for i,key in enumerate(pre_processed_collection_TIME):

        max_tf = Stats[key]['freq_max']
        tf = pre_processed_collection_TIME[key].count(word)
        TD_IDF[i,j] = (0.5 + 0.5*tf/max_tf) * idf


def article_word_tokenize(text):
    if type(text) != str:
        raise Exception("The function takes a string as input data")
    else:
        tokens = word_tokenize(text)
        return tokens


filename = ".\Data\Time\TIME.STP"
stop_words = []
with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if (line == ""):
            continue
        stop_words.append(line)


def remove_stop_words(query, stop_words):
    # TO COMPLETE
    filtered_words = []
    for word in query.split():
        if word not in stop_words:
            filtered_words.append(word)

    return filtered_words


query = remove_stop_words(query, stop_words)
print(query)


def transform_query_tf_idf(query):

    vectorize = np.zeros(len(Vocabulary))

    for j, word in enumerate(Vocabulary):
        df = 0
        for i, key in enumerate(pre_processed_collection_TIME):
            if word in pre_processed_collection_TIME[key]:
                df = df + 1

        idf = math.log(len(pre_processed_collection_TIME) / df, 10)

        stats = get_stats_document(query)
        max_tf = stats['freq_max']
        tf = query.count(word)

        vectorize[j] = (0.5 + 0.5*tf/max_tf) * idf

    return vectorize


query = transform_query_tf_idf(query)


def search_on_document_collection(query):

    results = np.zeros(len(pre_processed_collection_TIME))

    for i, key in enumerate(pre_processed_collection_TIME):
        document = TD_IDF[i, :]
        angle = np.dot(query, document)
        results[i] = angle

    results = np.argsort(results)[::-1]

    to_return = []
    for index in results:
        to_return.append(document_ids[index])
        if len(to_return) == 5:
            break

    return to_return


documents = search_on_document_collection(query)
print(documents)
for key in documents:
    print(pre_processed_collection_TIME[key])




