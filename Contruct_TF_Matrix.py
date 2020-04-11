import os
import nltk
import numpy as np
import math
import pickle as pkl
from tqdm import tqdm


root = "./pa1-data/"


tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
stop_words = nltk.corpus.stopwords.words('english')
lematizer = nltk.stem.WordNetLemmatizer()
steamer = nltk.stem.PorterStemmer()

Vocabulary = pkl.load(open("Vocabulary.pkl", "rb"))
Stats = pkl.load(open("Stats.pkl", "rb"))
Freq_Vocabulary = pkl.load(open("Freq_Vocabulary.pkl", "rb"))
Collection = pkl.load(open("Collection.pkl", "rb"))

break_point = 0
tokens = {}
for folder in os.listdir(root):

    path = root + folder
    for name in tqdm(os.listdir(path)):

        break_point = break_point + 1
        file_name = path + "/" + name
        file = open(file_name, 'r')

        for line in file:

            tokens[folder + "/" + name] = tokenizer.tokenize(line)

            text_no_stop_words = []
            for word in tokens[folder + "/" + name]:
                if word not in stop_words:
                    text_no_stop_words.append(word)

            text_no_stop_words = [lematizer.lemmatize(word) for word in text_no_stop_words]
            text_no_stop_words = [steamer.stem(word) for word in text_no_stop_words]
            tokens[folder + "/" + name] = text_no_stop_words


TF = {}
for document in tqdm(tokens):
    for word in tokens[document]:
        try:
            TF[document, word] = TF[document, word] + 1
        except KeyError:
            TF[document, word] = 1

pkl.dump(TF, open("TF.pkl","wb"))

