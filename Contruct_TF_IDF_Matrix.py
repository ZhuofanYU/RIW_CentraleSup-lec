import os
import nltk
import numpy as np
import math
import pickle as pkl
from tqdm import tqdm

Vocabulary = pkl.load(open("Vocabulary.pkl", "rb"))
Freq_Vocabulary = pkl.load(open("Freq_Vocabulary.pkl", "rb"))
Collection = pkl.load(open("Collection.pkl", "rb"))
TF = pkl.load(open("TF.pkl","rb"))

TF_IDF = {}
for key in tqdm(TF):

    word = key[1]
    idf = math.log(len(Collection)/Freq_Vocabulary[word], 10)
    TF_IDF[key] = TF[key] * idf


pkl.dump(TF_IDF, open("TF_IDF.pkl", "wb"))