import collections

"""
Regarder le nombre d'erreur par taille de mots
"""
X = []
y = []
with open("../data/fra4.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        X.append(ligne[0])
        y.append(ligne[1])

nbrErreur = {}
total = {}

for i in range(len(X)):
    sentence = X[i].split(" ")
    errors = y[i].split(" ")
    for j in range(len(sentence)):
        word = sentence[j]
        if errors[j] != "=":
            try:
                nbrErreur[len(word)] += 1
            except KeyError:
                nbrErreur[len(word)] = 1
        try:
            total[len(word)] += 1
        except KeyError:
            total[len(word)] = 1

#print(nbrErreur)
#print(total)

nbrErreur = collections.OrderedDict(sorted(nbrErreur.items()))
total = collections.OrderedDict(sorted(total.items()))
for k, v in total.items():
    try:
        print(k, v, nbrErreur[k], nbrErreur[k]/v*100)
    except:
        print(k, v, 0, 0)
