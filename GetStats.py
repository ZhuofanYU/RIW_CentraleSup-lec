import os
import nltk
import numpy as np
import math
import pickle as pkl
from tqdm import tqdm

root = "./pa1-data/"

documents = {}
tokens = {}
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
stop_words = nltk.corpus.stopwords.words('english')
lematizer = nltk.stem.WordNetLemmatizer()
steamer = nltk.stem.PorterStemmer()

"""
    Firstly we start be pre-processing all the collection 
    Removing stop words and lemmatizing things 
    This will prepare for the calculation of the tf-idf
"""
for folder in os.listdir(root):

    path = root + folder
    for name in tqdm(os.listdir(path)):

        file_name = path + "/" + name
        file = open(file_name, 'r')

        i = 0
        for line in file:

            documents[folder + "/" + name] = line
            tokens[folder + "/" + name] = tokenizer.tokenize(line)

            text_no_stop_words = []
            for word in tokens[folder + "/" + name]:
                if word not in stop_words:
                    text_no_stop_words.append(word)

            text_no_stop_words = [lematizer.lemmatize(word) for word in text_no_stop_words]
            text_no_stop_words = [steamer.stem(word) for word in text_no_stop_words]
            tokens[folder + "/" + name] = text_no_stop_words


Vocabulary = pkl.load(open("Vocabulary.pkl", "rb"))


def get_stats_document(document):
    """
        Get the statistics for each document!!!!
    """
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
    for key in tqdm(collection):
        stats[key] = get_stats_document(collection[key])

    return stats

"""
    Get the stats for the collection
"""
Stats = get_stats_collection(tokens)


"""
    Get the stats for the vocabulary
"""
Freq_Vocabulary = {}
for word in tqdm(Vocabulary):
    Freq_Vocabulary[word] = 0

for key in tokens:
    words_so_far = []
    for word in tokens[key]:
        if word not in words_so_far:
            Freq_Vocabulary[word] = Freq_Vocabulary[word] + 1
            words_so_far.append(word)

for key in Stats:
    print(key, Stats[key])

for key in Freq_Vocabulary:
    print(key, Freq_Vocabulary[key])

pkl.dump(Stats, open("Stats.pkl", "wb"))
pkl.dump(Freq_Vocabulary, open("Freq_Vocabulary.pkl", "wb"))