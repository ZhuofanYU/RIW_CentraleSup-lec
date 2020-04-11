import pickle as pkl

with open("TF.pkl", "rb") as f:
    TF1 = pkl.load(f)
    TF2 = pkl.load(f)

for key in TF1:
    print(key)

for key in TF2:
    print(key)
