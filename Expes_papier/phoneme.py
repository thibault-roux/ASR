from wer import cer
from statistics import mean
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn


def phoneme_analysis(id):
    phons = "<eps> k p l t R f s d Z n b v g m z S N G x a E § j o O i 1 5 e u @ ° 9 w y 8 2".split(" ")
    matrix = dict()
    for p in phons:
        matrix[p] = dict()
        for p_ in phons:
            matrix[p][p_] = 0

    ref = []
    hyp = []
    with open("data/SP7.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne.split("\t")
            ref.append(ligne[0])
            hyp.append(ligne[1])

    per = []
    for i in range(len(ref)):
        """if i%500 == 0:
            print(i)"""
        try:
            r, h, list, result = cer(ref[i], hyp[i])
            per.append(result)
        except MemoryError:
            print("Erreur, n'a pas fonctionné pour :")
            print(ref[i])
            print(hyp[i])
            print(i)
            continue
        if len(r) != len(h):
            print("Erreur, la référence et l'hypothèse n'ont pas la même longueur")
            print(ref[i])
            print(hyp[i])
        for j in range(len(r)):
            matrix[r[j]][h[j]] += 1
    """for k, v in matrix.items():
        if v != []:
            print(k, v)"""
    pickle.dump(matrix, open("pickle/PHON_matrix" + id + ".pickle", "wb"))
    return mean(per)




def plotConfusion(id):
    phon_matrix = pickle.load(open("pickle/PHON_matrix" + id + ".pickle", "rb"))
    phon_possible = "<eps> k p l t R f s d Z n b v g m z S N G x a E § j o O i 1 5 e u @ ° 9 w y 8 2".split(" ")
    real_phonemes = "<eps> k p l t ʁ f s d ʒ n b v g m z ʃ ɲ ɳ x a ɛ ɔ~ j o ɔ i œ~ ɛ~ e u ɑ~ ə œ w y ɥ ø".split(" ")

    matrix = []
    i = 0
    for k, v in phon_matrix.items():
        row = []
        if k != phon_possible[i]:
            print("ERREUR!!!")
        for j in phon_possible:
            row.append(v[j])
        matrix.append(row)
        i += 1
    matrix = np.array(matrix)
    mat2 = matrix.copy() #.astype(np.float32)
    for i in range(matrix.shape[0]):
        somme = np.sum(matrix[i])
        for j in range(matrix.shape[1]):
            if somme != 0:
                mat2[i][j] = round(matrix[i][j]/somme*100)
    #renamed
    renamed = dict()
    for i in range(len(phon_possible)):
        renamed[i] = real_phonemes[i]

    df_cm = pd.DataFrame(mat2, range(matrix.shape[0]), range(matrix.shape[0]))
    df_cm = df_cm.rename(columns=renamed)
    df_cm = df_cm.rename(index=renamed)
    plt.figure(figsize=(22,16))
    sn.set(font_scale=1.0) # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 12}) # font size
    plt.savefig("results/PHON_confusion_matrix_percent_" + id + ".png")
