import os
import nltk
import numpy as np
import math
import pickle as pkl

root = "./pa1-data/"

break_factor = 0
documents = {}
tokens = {}
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
stop_words = nltk.corpus.stopwords.words('english')
steamer = nltk.stem.WordNetLemmatizer()

"""
    Firstly we start be pre-processing all the collection 
    Removing stop words and lemmatizing things 
    This will prepare for the calculation of the tf-idf
"""
for folder in os.listdir(root):

    path = root + folder
    for name in os.listdir(path):

        file_name = path + "/" + name
        file = open(file_name, 'r')

        i = 0
        for line in file:
            """
            if break_factor == 10:
                break
            """
            break_factor = break_factor + 1

            documents[name] = line
            tokens[name] = tokenizer.tokenize(line)

            text_no_stop_words = []
            for word in tokens[name]:
                if word not in stop_words:
                    text_no_stop_words.append(word)

            text_no_stop_words = [steamer.lemmatize(word) for word in text_no_stop_words]
            tokens[name] = text_no_stop_words


"""
    Get the vocabulary from the collection
"""
def get_vocabulary(collection):
    vocabulary = []

    for key in collection:
        for word in collection[key]:
            if word not in vocabulary:
                vocabulary.append(word)

    return vocabulary


"""
    Here we extract the vocabulary from the collection!
"""
Vocabulary = get_vocabulary(tokens)


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
    for key in collection:
        stats[key] = get_stats_document(collection[key])

    return stats


"""
    Get the stats for the collection
"""
Stats = get_stats_collection(tokens)
TF_IDF = np.zeros((len(tokens),len(Vocabulary)))

"""
    Get the tf-idf matrix for the collection!
"""
for j,word in enumerate(Vocabulary):

    df = 0
    for i,key in enumerate(tokens):
        if word in tokens[key]:
            df = df + 1

    idf = math.log(len(tokens) / df, 10)

    for i,key in enumerate(tokens):

        max_tf = Stats[key]['freq_max']
        tf = tokens[key].count(word)
        TF_IDF[i,j] = (0.5 + 0.5*tf/max_tf) * idf

"""
    To deal with this matrix we need two things!!!!
    Dictionary that converts index in name
    Dictionary that converts name in index
"""
index_to_name = {}
name_to_index = {}
for i,key in enumerate(documents):
    index_to_name[i] = key
    name_to_index[key] = i

Storage = {}
Storage["index_to_name"] = index_to_name
Storage["name_to_index"] = name_to_index
Storage["documents"] = documents
Storage["TF_IDF"] = TF_IDF
pkl.dump(Storage, open("Storage.pkl", "wb"))
print(TF_IDF)