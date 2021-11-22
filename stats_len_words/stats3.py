import collections
from jiwer import cer
from statistics import mean
X = []
y = []
with open("../data/fra7.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        X.append(ligne[0])
        y.append(int(ligne[1]))

dict = {} #{0: [3, 1, 3], 1: [2, 2, 5, 3]
#nombre d'erreurs, taille des mots
for i in range(len(X)):
    sentence = X[i].split(" ")
    for word in sentence:
        try:
            dict[y[i]].append(len(word))
        except KeyError:
            dict[y[i]] = [len(word)]

dict = collections.OrderedDict(sorted(dict.items()))
for k, v in dict.items():
    print(k, mean(v), len(v))
