import os
from tqdm import tqdm
import pickle as pkl


root = "./pa1-data/"

"""
    In this file we gather all the names of the files in the collection
    This is used to access them in other programs
"""
Collection = []
for folder in os.listdir(root):

    path = root + folder
    for name in tqdm(os.listdir(path)):
        Collection.append(folder + "/" + name)

print(Collection)
pkl.dump(Collection, open("Collection.pkl","wb"))
