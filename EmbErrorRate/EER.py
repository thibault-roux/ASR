import numpy as np
from scipy import spatial

#embeddings:
namefile = "../../../Stage/embeddings_fast_text/cc.fr.300.vec"
#namefile = "../../../Stage/embeddings_fast_text/temp.vec"

ref = []
hyp = []
refhyp = set()
with open("../data/fra8.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        r = ligne[0].lower()
        h = ligne[1].lower()
        ref.append(r)
        hyp.append(h)

        for e in r.split(" "):
            refhyp.add(e)
        for e in h.split(" "):
            refhyp.add(e)

print("Chargement des embeddings...")
tok2emb = {}
"""
file = open(namefile, "r", encoding="utf8")
fread = file.readlines()
for i in range(1, len(fread)):
    ligne = fread[i]
"""
file = open(namefile, "r", encoding="utf8") #l'ajout débute ici
next(file)
for ligne in file: #l'ajout est jusqu'ici
    ligne = ligne[:-1].split(" ")
    if ligne[0] in refhyp:
        emb = np.array(ligne[1:]).astype(float)
        if emb.shape != (300,):
            print("Erreur à " + ligne[0])
        else:
            tok2emb[ligne[0]] = emb
print("Embeddings chargés.")

"""
for k in tok2emb.keys():
    print(k)
"""

def similarite(syn1, syn2):
    try:
        return 1 - spatial.distance.cosine(syn1, syn2)
    except KeyError:
        return 0

voc = tok2emb.keys()
#Calcul du Embedding Error Rate
print("Calcul du Embedding Error Rate...")
errors = []
for i in range(len(ref)):
    if i %100 == 0:
        print(i)
    error = []
    r = ref[i].split(" ")
    h = hyp[i].split(" ")
    for j in range(len(r)):
        if r[j] != h[j]:
            if r[j] == "<eps>" or h[j] == "<eps>":
                error.append(1)
            else:
                if r[j] in voc and h[j] in voc:
                    #error.append(1 + -1*similarite(tok2emb[r[j]], tok2emb[h[j]])) #comment j'utilise cette similarité ?
                    if similarite(tok2emb[r[j]], tok2emb[h[j]]) > 0.4:
                        error.append(0.1)
                        print(r[j])
                        print(h[j])
                else:
                    error.append(1)
        else:
            error.append(0)
    errors.append(error)

import pickle

print()
print(len(errors))
pickle.dump(errors, open("errors.pickle", "wb"))

s = 0
length = 0
for i in range(len(errors)):
    s += sum(errors[i])
    length += len(errors[i])

print(s/length)
