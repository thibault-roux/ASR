from jiwer import wer
import pickle
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from EER import eer
#from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from statistics import mean
from phoneme import phoneme_analysis
from phoneme import plotConfusion

import argparse
parser = argparse.ArgumentParser(description="Launch a serie of experiment")
parser.add_argument("id", type=str, help="ID (SP, KD, etc...)")
args = parser.parse_args()


"""
 - exp1: Calculer le POS error Rate avec SP4.txt (sans <eps>)
 - exp2: Calculer la confusion matrix de POS avec SP4.txt (avec <eps) -> ATTENTION: l'exp2 est calculé automatiquement lors de la création de SP4
 - exp3: Calculer le CER par POS avec SP5.txt (avec <eps>)
 - exp4: Calculer le n-gram de POS avec SP6.txt (sans <eps>)
 - exp5: Calculer le EmbeddingErrorRate avec SP1.txt (avec <eps>)
 - exp6: Utiliser la similarité BERT avec SP1.txt (sans <eps>)
 - exp7: Calculer le phonème error rate avec SP7.tt
 - exp8: Calculer la confusion matrix de phonème avec SP7.txt
 - exp9: Régression du nombre d'erreur avec SP2.txt (sans <eps>)
"""

def retirerEPS(ligne):
    retour = ""
    ligne = ligne.split(" ")
    for i in range(len(ligne)):
        if ligne[i] != "<eps>":
            retour += ligne[i] + " "
    return retour[:-1]

fresults = open("results/" + args.id + ".txt", "w", encoding="utf8")

"""---------------exp1-POS_error_rate---------------"""
#4 sans eps
wers = []
with open("data/" + args.id + "4.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        if retirerEPS:
            ligne[0] = retirerEPS(ligne[0])
            ligne[1] = retirerEPS(ligne[1])
        wers.append(wer(ligne[0], ligne[1]))

fresults.write("POS Error Rate: " + str(sum(wers)/len(wers)) + "\n")


"""---------------exp2-POS_confusion_matrix---------------"""
#4 avec eps
POS_matrix = pickle.load(open("pickle/POS_matrix" + args.id + ".pickle", "rb"))
POS_possible = ["ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","PUNCT","SCONJ","SYM","VERB","X", "<eps>"] #à adapter selon besoin
matrix = []
i = 0
for k, v in POS_matrix.items():
    row = []
    if k != POS_possible[i]:
        fresult.write("ERREUR lors de l'expérience 2.\n")
    for j in range(len(POS_possible)):
        row.append(v.count(POS_possible[j]))
    matrix.append(row)
    i += 1
matrix = np.array(matrix)
mat2 = matrix.copy()
for i in range(matrix.shape[0]):
    somme = np.sum(matrix[i])
    for j in range(matrix.shape[1]):
        if somme != 0:
            mat2[i][j] = round(matrix[i][j]/somme*100)
renamed = dict()
for i in range(len(POS_possible)):
    renamed[i] = POS_possible[i]
df_cm = pd.DataFrame(mat2, range(matrix.shape[0]), range(matrix.shape[0]))
df_cm = df_cm.rename(columns=renamed)
df_cm = df_cm.rename(index=renamed)
plt.figure(figsize=(20,14))
sn.set(font_scale=1.4) # for label size
sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
plt.savefig("results/POS_confusion_matrix_percent_" + args.id + ".png")
fresults.write("La POS confusion matrix de " + args.id + " a été enregistré dans /results.\n")



"""---------------exp3-CER_POS---------------"""
#5 avec eps
fresults.write("Le CER moyen par POS n'a pas été calculé.\n")


"""---------------exp4-Ngram_POS---------------"""
#6 sans eps
fresults.write("Les n-gram de POS les plus sujets aux erreurs n'ont pas été calculé.\n")


"""---------------exp5-EER----------------"""
#1 avec eps
#fresults.write("Embedding Error Rate avec mauvais embeddings : " + str(eer(args.id)) + "\n")


"""---------------exp6-Similarity_Contextual---------------"""
#1 sans eps
"""
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
sims = []
ind = 0
with open("data/" + args.id + "1.txt", "r", encoding="utf8") as file:
    for ligne in file:
        print(ind)
        ind += 1
        ligne = ligne.split("\t")
        ligne[0] = retirerEPS(ligne[0])
        ligne[1] = retirerEPS(ligne[1])
        ligne0 = [ligne[0].lower()]
        ligne1 = [ligne[1].lower()]
        if ligne0 != ligne1:
            ligne0 = model.encode(ligne0)
            ligne1 = model.encode(ligne1)
            sims.append(cosine_similarity(ligne0, ligne1)[0][0])
        else:
            sims.append(1)
pickle.dump(sims, open("pickle/sims" + args.id + ".pickle", "wb"))
fresults.write("Average Similarity : " + str(mean(sims)) + " (Stored in sims" + args.id + ".pickle)\n")
"""

"""---------------exp7-Phoneme_Error_Rate---------------"""
#7 sans eps
per = phoneme_analysis(args.id)
fresults.write("Phoneme Error Rate : " + str(per) + "%\n")

"""---------------exp8-Phoneme_confusion_matrix---------------"""
#7 avec eps
plotConfusion(args.id)
fresults.write("La phoneme confusion matrix de " + args.id + " a été enregistré dans /results.\n")

"""---------------exp9-regression_nombre_erreur---------------"""
#2 sans eps



fresults.close()
