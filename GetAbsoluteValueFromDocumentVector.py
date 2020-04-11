import pickle as pkl
import math

Collection = pkl.load(open("Collection.pkl", "rb"))
TF_IDF = pkl.load(open("TF_IDF.pkl","rb"))

print(Collection)
Absolute_Value = {}
for document in Collection:
    Absolute_Value[document] = 0

for key in TF_IDF:
    Absolute_Value[key[0]] = Absolute_Value[key[0]] + TF_IDF[key]**2

for document in Absolute_Value:
    Absolute_Value[document] = math.sqrt(Absolute_Value[document])

pkl.dump(Absolute_Value, open("Absolute_Values.pkl", "wb"))