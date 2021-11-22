import collections
from jiwer import cer

"""
Regarder le nombre d'erreur par taille de mots
Faire un histogramme
"""
X = []
y = []
with open("../data/fra8.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        X.append(ligne[0])
        y.append(ligne[1])


dict = {}

for i in range(len(X)):
    sentence1 = X[i].split(" ")
    sentence2 = y[i].split(" ")
    for j in range(len(sentence1)):
        try:
            word1 = sentence1[j]
            word2 = sentence2[j]
        except:
            print(i)
            print(sentence1)
            print(sentence2)
            print(len(sentence1))
            print(len(sentence2))
            print(j)
            exit()
        #interpréter les <eps> haut comme un mot de taille 0
        #avec une erreur de taille mot du bas.

        #interpréter les <eps> bas comme un mot de taille len(mot du haut)
        #avec une erreur de taille mot du haut
        if word1 == "<eps>":
            try:
                dict[0].append(len(word2))
            except KeyError:
                dict[0] = [len(word2)]
        if word2 == "<eps>":
            try:
                dict[len(word1)].append(len(word1))
            except KeyError:
                dict[len(word1)] = [len(word1)]
        dist = cer(word1, word2)*len(word1)
        try:
            dict[len(word1)].append(dist)
        except KeyError:
            dict[len(word1)] = [dist]


dict = collections.OrderedDict(sorted(dict.items()))
for k, v in dict.items():
    print(k, v)

import pickle

pickle.dump(dict, open("dict.pickle", "wb"))
