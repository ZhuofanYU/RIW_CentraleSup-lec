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

break_point = 0
for folder in os.listdir(root):

    path = root + folder
    for name in tqdm(os.listdir(path)):
        break_point = break_point + 1

        file_name = path + "/" + name
        file = open(file_name, 'r')

        for line in file:

            documents[name] = line
            tokens[name] = tokenizer.tokenize(line)

            text_no_stop_words = []
            for word in tokens[name]:
                if word not in stop_words:
                    text_no_stop_words.append(word)

            text_no_stop_words = [lematizer.lemmatize(word) for word in text_no_stop_words]
            text_no_stop_words = [steamer.stem(word) for word in text_no_stop_words]
            tokens[name] = text_no_stop_words


def get_vocabulary(collection):
    """
        Get the vocabulary from the collection
    """
    vocabulary = []

    for key in tqdm(collection):
        for word in collection[key]:
            if word not in vocabulary:
                vocabulary.append(word)

    return vocabulary


"""
    Here we extract the vocabulary from the collection!
"""
Vocabulary = get_vocabulary(tokens)

print(len(documents))
print(len(Vocabulary))

pkl.dump(Vocabulary, open("Vocabulary.pkl", "wb"))
