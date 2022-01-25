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
from Levenshtein import distance as lv

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



"""-------------Choix automatique des POS---------------"""
temp_pos = set()
with open("data/" + args.id + "4.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        for pos in ligne[1].split(" "):
            temp_pos.add(pos)
POS_possible1 = ['PPER1S', 'VERB', 'COSUB', 'PUNCT', 'PREP', 'PDEMMS', 'COCO', 'DET', 'NMP', 'ADJMP', 'PREL', 'PREFP', 'AUX', 'ADV', 'VPPMP', 'DINTMS', 'ADJMS', 'NMS', 'NFS', 'YPFOR', 'PINDMS', 'NOUN', 'PROPN', 'DETMS', 'PPER3MS', 'VPPMS', 'DETFS', 'ADJFS', 'ADJFP', 'NFP', 'VPPFS', 'CHIF', 'XFAMIL', 'PPER3MP', 'PPOBJMS', 'PREF', 'PPOBJMP', 'SYM', 'DINTFS', 'PDEMFS', 'PPER3FS', 'VPPFP', 'PRON', 'PPOBJFS', 'PART', 'PPER3FP', 'MOTINC', 'PDEMMP', 'INTJ', 'PREFS', 'ADJ', 'PINDMP', 'PINDFS', 'NUM', 'PPER2S', 'PPOBJFP', 'PDEMFP', 'X', 'PRELMS', 'PINDFP', "<eps>"]
POS_possible1.sort()
POS_possible2 = ["<eps>", "ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","PUNCT","SCONJ","SYM","VERB","X"] #à adapter selon besoin
POS_possible = []
for e in temp_pos:
    POS_possible.append(e)
POS_possible.sort()
if POS_possible != POS_possible1 and POS_possible != POS_possible2:
    print("Les POS détectés automatiquement ne sont pas habituelles.")
    print(POS_possible)
    answer = input("Continuer quand même ? (o/n) : ")
    if answer == "n":
        print("Le programme s'est terminé sous demande.")
        exit(0)
    elif answer != "o":
        print("Réponse non attendue. Fin du programme.")
        exit(0)


"""---------------exp0-Word_error_rate---------------"""
with open("data/" + args.id + "2.txt", "r", encoding="utf8") as file:
    total = 0
    errors = 0
    for ligne in file:
        for err in ligne.split("\t")[2].split(" "): #pour chaque erreur (S I =)
            if err != "=":
                errors += 1
            if err != "I": #Les insertions ne sont pas comptabilisés dans le total des mots
                total += 1
fresults.write("Word Error Rate: ")
a = "{:.2f}".format(float(errors/total)*100)
fresults.write(a)
fresults.write("\n")


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
matrix = []
i = 0
for k, v in POS_matrix.items():
    row = []
    if k != POS_possible[i]:
        fresults.write("ERREUR lors de l'expérience 2.\n")
        break
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
#ce que je vais stocker, c'est un dictionnaire de POS qui contient une liste de liste de deux (cer et taille du mot)
#ça permettra de faire des analyses de la répartition des tailles des POS
CER_POS = dict()
for e in POS_possible:
    if e != "<eps>":
        CER_POS[e] = []
with open("data/SP5.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        pos = ligne[1].split(" ")
        ref = ligne[2].split(" ")
        hyp = ligne[3].split(" ")
        if len(ref) == len(hyp) and len(ref) == len(pos):
            for i in range(len(ref)):
                if ref[i] != "<eps>" and hyp[i] != "<eps>":
                    distance = lv(ref[i], hyp[i]) #distance de Levenshtein
                    CER_POS[pos[i]].append([distance, len(ref[i])])
txt = "CER moyen par POS :"
for k, v in CER_POS.items():
    if v != []:
        cers = 0
        total = 0
        for tuple in v:
            cers += tuple[0]
            total += tuple[1]
        txt += k + ": " + str(cers/total*100) + ", "
fresults.write(txt[:-2])


"""
Questions soulevées par cette expérience :
- Comment doit-on traiter les <eps> ?
    -> J'ai décidé de les ignorer. On ne regarde que les substitutions.
- Il y a 88 phrases qui n'ont pas la bonne longueur.
    -> Je les ignore vu qu'elles ne représentent quasiment rien par rapport à 106863 phrases.
- Ce CER moyen par POS n'est pas la moyenne des CER pour chaque mot mais la somme des distances divisé par la somme des tailles de mots.
"""



"""---------------exp4-Ngram_POS---------------"""
#6 sans eps
fresults.write("Les n-gram de POS les plus sujets aux erreurs n'ont pas été calculé.\n")
def ngram_pos(n):
    ngram = dict()
    with open("data/" + id + "6.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne.split("\t")
            pos = ligne[1].split(" ")
            err = ligne[2].split(" ")
            if len(pos) == len(err):
                if len(pos) >= n:
                    i = 0
                    while (i + n) < len(pos):
                        j = 0
                        gram = []
                        errs = []
                        while j < n:
                            gram.append(pos[i+j])
                            errs.append(err[i+j])
                            j += 1
                        i += 1
#ngram_pos(3)

"""
Questions soulevées par cette expérience :
- Comment doit-on traiter les <eps> ?
    -> Quand il y a une insertion (i.e un <eps> dans la réf)
- Est-ce que je stocke le nombre d'erreur ? Ou directement les types d'erreurs ?
    -> je peux avoir APD DET NOUN : [[S,S,=], [D,=,=], [=,=,=]]
    -> ou ADP DET NOUN : {S: 10, D:2, I:3, =:40}
    -> ou ADP DET NOUN : [23, 130] #avec première valeur == erreur et deuxième valeur == total
- Il faudrait que je sorte des exemples de ces suites de POS (avec leur mot associé)
- Le ngram impose qu'on ignore les utterances plus courtes que n
    -> pour n = 3, il y a 222 utterances éliminés pour cette raison
"""


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
"""
per = phoneme_analysis(args.id)
fresults.write("Phoneme Error Rate : " + str(per) + "%\n")
"""

"""---------------exp8-Phoneme_confusion_matrix---------------"""
#7 avec eps
"""
plotConfusion(args.id)
fresults.write("La phoneme confusion matrix de " + args.id + " a été enregistré dans /results.\n")
"""

"""---------------exp9-regression_nombre_erreur---------------"""
#2 sans eps



fresults.close()
