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
from EER import eer

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
 -exp10: Lemme Error Rate
 -exp11: N-gram de mots
 -exp12: Mot avec le plus d'erreurs
 -exp13: Top confusion pairs
 -exp14: Substitution Confusion Matrix
"""


"""--------------Choix des expériences---------------"""
launch_expes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
remove = [6, 7, 8, 9, 10, 11] #suppression des expes
#avec assez de RAM, il faut garder l'expérience 6
for r in remove:
    launch_expes.remove(r)



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
with open("data/" + args.id + "/" + args.id + "4.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        for pos in ligne[1].split(" "):
            temp_pos.add(pos)
POS_possible1 =['ADJ', 'ADJFP', 'ADJFS', 'ADJMP', 'ADJMS', 'ADV', 'AUX', 'CHIF', 'COCO', 'COSUB', 'DET', 'DETFS', 'DETMS', 'DINTFS', 'DINTMS', 'INTJ', 'MOTINC', 'NFP', 'NFS', 'NMP', 'NMS', 'NOUN', 'NUM', 'PART', 'PDEMFP', 'PDEMFS', 'PDEMMP', 'PDEMMS', 'PINDFP', 'PINDFS', 'PINDMP', 'PINDMS', 'PPER1S', 'PPER2S', 'PPER3FP', 'PPER3FS', 'PPER3MP', 'PPER3MS', 'PPOBJFP', 'PPOBJFS', 'PPOBJMP', 'PPOBJMS', 'PREF', 'PREFP', 'PREFS', 'PREL', 'PRELFP', 'PRELFS', 'PRELMP', 'PRELMS', 'PREP', 'PRON', 'PROPN', 'PUNCT', 'SYM', 'VERB', 'VPPFP', 'VPPFS', 'VPPMP', 'VPPMS', 'X', 'XFAMIL', 'YPFOR', '<eps>']
POS_possible1.sort()
POS_possible2 = ["<eps>", "ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","PUNCT","SCONJ","SYM","VERB","X"] #à adapter selon besoin
POS_possible = []
for e in temp_pos:
    POS_possible.append(e)
POS_possible.sort()
if POS_possible != POS_possible1 and POS_possible != POS_possible2:
    print("Les POS détectés automatiquement ne sont pas habituelles. Nous avons sélectionné automatiquement ces POS :")
    if (len(POS_possible)-len(POS_possible2))**2 < (len(POS_possible)-len(POS_possible2))**2:
        POS_possible = POS_possible2
    else:
        POS_possible = POS_possible1
    print(POS_possible)
    answer = input("Continuer quand même ? (o/n) : ")
    if answer == "n":
        print("Le programme s'est terminé sous demande.")
        exit(0)
    elif answer != "o":
        print("Réponse non attendue. Fin du programme.")
        exit(0)

"""-------------Mapper-POS---------------"""
#Les POS étendues sont trop nombreuses pour être visualisés facilement. J'utilise donc un mapping pour réduire le nombre de classes aux Upos
mapper = dict()
mapper["<eps>"] = "<eps>"
mapper[''] = ''
with open("mapping.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne[:-1].split("\t")
        mapper[ligne[0]] = ligne[1]







"""---------------exp0-Word_error_rate---------------"""
if 0 in launch_expes:
    with open("data/" + args.id + "/" + args.id + "2.txt", "r", encoding="utf8") as file:
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
if 1 in launch_expes:
    wers = []
    with open("data/" + args.id + "/" + args.id + "4.txt", "r", encoding="utf8") as file:
        gt = []
        hp = []
        for ligne in file:
            ligne = ligne.split("\t")
            ref = retirerEPS(ligne[1])
            hyp = retirerEPS(ligne[2])
            gt.append(ref)
            hp.append(hyp)
    fresults.write("POS Error Rate: " + str(wer(gt, hp)) + "\n")
    wers = []
    with open("data/" + args.id + "/" + args.id + "4.txt", "r", encoding="utf8") as file:
        gt = []
        hp = []
        for ligne in file:
            ligne = ligne.split("\t")
            ref = retirerEPS(ligne[1]).split(" ")
            hyp = retirerEPS(ligne[2]).split(" ")
            for i in range(len(ref)):
                ref[i] = mapper[ref[i]]
            for i in range(len(hyp)):
                hyp[i] = mapper[hyp[i]]
            ref = " ".join(ref)
            hyp = " ".join(hyp)
            gt.append(ref)
            hp.append(hyp)
    fresults.write("uPOS Error Rate: " + str(wer(gt, hp)) + "\n")


"""---------------exp2-POS_confusion_matrix---------------"""
#4 avec eps
if 2 in launch_expes:
    POS_matrix = pickle.load(open("pickle/POS_matrix" + args.id + ".pickle", "rb"))
    POS_matrix_extended = pickle.load(open("pickle/POS_matrix" + args.id + ".pickle", "rb"))
    POS_matrix = dict()
    for k, v in POS_matrix_extended.items():
        POS_matrix[mapper[k]] = []
        for i in range(len(v)):
            POS_matrix[mapper[k]].append(mapper[v[i]])

    old = POS_possible
    POS_possible = POS_possible2
    matrix = []
    i = 0
    keys = list(POS_matrix.keys())
    keys.sort()
    #for k, v in POS_matrix.items():
    for k in keys:
        v = POS_matrix[k]
        row = []
        if k != POS_possible[i]:
            print(POS_possible)
            print(POS_matrix.keys())
            print(k)
            fresults.write("ERREUR lors de l'expérience 2.\n")
            exit(-1)
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
    POS_possible = old


"""---------------exp3-CER_POS---------------"""
#5 avec eps
#ce que je vais stocker, c'est un dictionnaire de POS qui contient une liste de liste de deux (cer et taille du mot)
#ça permettra de faire des analyses de la répartition des tailles des POS
if 3 in launch_expes:
    CER_POS = dict()
    for e in POS_possible:
        if e != "<eps>":
            CER_POS[e] = []
    with open("data/" + args.id + "/" + args.id + "5.txt", "r", encoding="utf8") as file:
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
    txt = "CER moyen par POS: "
    for k, v in CER_POS.items():
        if v != []:
            cers = 0
            total = 0
            for tuple in v:
                cers += tuple[0]
                total += tuple[1]
            txt += k + ": " + str(cers/total*100) + "%, "
    pickle.dump(CER_POS, open("pickle/CER_POS" + args.id + ".pickle", "wb"))
    fresults.write(txt[:-2] + "\n")


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
if 4 in launch_expes:
    from bisect import bisect_right as bisect

    class Pool:
        def __init__(self, maxsize, min_occ, n):
            self.maxsize = maxsize
            self.min_occ = min_occ
            self.n = n
            self.p = [] #liste de ratio
            self.keys = []

        def add(self, k, v):
            total = 0
            incorrect = 0
            for errs in v: #v est une liste de liste d'erreurs [[= = =], [S = =], [S S S], [S = I =], etc]
                for err in errs: #liste d'erreur [= S =]
                    total += 1
                    if err != "=":
                        incorrect += 1
            ratio = incorrect/total
            b = bisect(self.p, ratio)
            """if b < self.maxsize:
                self.p.insert(b, ratio)
                self.keys.insert(b, k)"""
            self.p.insert(b, ratio)
            self.keys.insert(b, k)
            self.p = self.p[-self.maxsize:]
            self.keys=self.keys[-self.maxsize:]

        def print(self):
            txt = "Top " + str(self.maxsize) + " des " + str(self.n) + "-grams de uPOS les plus sujets aux erreurs occurant au moins " + str(self.min_occ) + " fois: "
            for i in range(self.maxsize-1, -1, -1):
                txt += str(self.keys[i]) + " " + str(self.p[i]) + ", "
            txt = txt[:-2] + "\n"
            return txt

    def bests(dico, top=10, min_occ=38, n=3): #on cherche les n-grams les plus coûteux
        pool = Pool(maxsize=top, min_occ=min_occ, n=n)
        for k, v in dico.items():
            if len(v) > min_occ:
                pool.add(k, v)
        return pool.print()

    def add_N(dico, gram, err):
        gram = " ".join(gram)
        #err = " ".join(err)
        if gram in dico:
            dico[gram].append(err)
        else:
            dico[gram] = []
            dico[gram].append(err)

    def ngram_pos(n):
        ngram = dict()
        with open("data/" + args.id + "/" + args.id + "6.txt", "r", encoding="utf8") as file:
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
                            compteur = 0
                            #utiliser un compteur qui augmente à chaque <eps> de la réf
                            while True: #j < (n+compteur)
                                if pos[i+j] == "<eps>":
                                    compteur += 1
                                else:
                                    gram.append(mapper[pos[i+j]])
                                errs.append(err[i+j])
                                j += 1
                                if j >= (n+compteur) or (i+j) >= len(pos):
                                    break
                            add_N(ngram, gram, errs)
                            i += 1

        pickle.dump(ngram, open("pickle/POS_ngram" + args.id + ".pickle", "wb"))
        return bests(ngram, top=10, min_occ=38, n=n)

    fresults.write(ngram_pos(3))

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
if 5 in launch_expes:
    #fresults.write("Embedding Error Rate avec mauvais embeddings : " + str(eer(args.id)) + "\n")
    fresults.write("EER: " + str(eer(args.id)) + "\n")


"""---------------exp6-Similarity_Contextual---------------"""
#1 sans eps
if 6 in launch_expes:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    sims = []
    ind = 0
    with open("data/" + args.id + "/" + args.id + "1.txt", "r", encoding="utf8") as file:
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


"""---------------exp7-Phoneme_Error_Rate---------------"""
#7 sans eps
if 7 in launch_expes:
    per = phoneme_analysis(args.id)
    fresults.write("Phoneme Error Rate : " + str(per) + "%\n")


"""---------------exp8-Phoneme_confusion_matrix---------------"""
#7 avec eps
if 8 in launch_expes:
    plotConfusion(args.id)
    fresults.write("La phoneme confusion matrix de " + args.id + " a été enregistré dans /results.\n")


"""---------------exp9-regression_nombre_erreur---------------"""
#2 sans eps
if 9 in launch_expes:
    pass

"""--------------exp12-top-error-rate-------------------------"""
if 12 in launch_expes:
    class MotsErrors:
        def __init__(self):
            self.mots = dict()
        def add_error(self, mot):
            if mot in self.mots:
                self.mots[mot][1] += 1
            else:
                self.mots[mot] = [0, 1]
        def add(self, mot):
            if mot in self.mots:
                self.mots[mot][0] += 1
            else:
                self.mots[mot] = [1, 0]
        def top_wrong(self, n=10, min_occ=30):
            n += 1 #pour ignorer <eps>
            bests = []
            copy = self.mots
            for i in range(n):
                max = -1
                max_k = "NaN"
                v1 = -1
                v0 = -1
                for k, v in copy.items():
                    if v[0] > min_occ:
                        newm = v[1]/v[0]
                        if newm > max:
                            max_k = k
                            max = newm
                            v1 = v[1]
                            v0 = v[0]
                copy[max_k] = [-1, -1]
                bests.append([max_k, v1, v0, max])
            return bests
        def mediane(self): #retourne la médiane des occurences
            occurences = []
            for k, v in self.mots.items():
                occurences.append(v[0])
                #v = [43, 8] #43 occurences pour 8 erreurs
            occurences.sort()
            #print(occurences[int(len(occurences)/2)])

    mots_errors = MotsErrors()
    with open("data/" + args.id + "/" + args.id + "2.txt", "r", encoding="utf8") as file:
        ref = []
        err = []
        for ligne in file:
            ligne = ligne.split("\t")
            ref.append(ligne[1].split(" "))
            err.append(ligne[2].split(" "))
    for i in range(len(ref)):
        if len(ref[i]) == len(err[i]):
            for j in range(len(ref[i])):
                mot = ref[i][j]
                if err[i][j] != "=":
                    mots_errors.add_error(mot)
                mots_errors.add(mot)

    top = 10
    min_occ = 300
    bests = mots_errors.top_wrong(n=top, min_occ=min_occ)
    txt = "Top " + str(top) + " des mots avec le plus d'erreur apparaissant au moins " + str(min_occ) + " fois: "
    for i in range(1, len(bests)):
        txt += "[" + bests[i][0] + ", " + str(bests[i][-1]) + "], "
        #print(bests[i][0], bests[i][1], bests[i][2], bests[i][-1])
    txt = txt[:-2] + "\n"
    fresults.write(txt)


"""--------------exp13-top-confusion-pairs-------------------------"""
if 13 in launch_expes:
    from collections import Counter
    substitutions = []
    with open("data/" + args.id + "/" + args.id + "1.txt", "r", encoding="utf8") as file:
        ref = []
        hyp = []
        for ligne in file:
            ligne = ligne.split("\t")
            ref.append(ligne[1].split(" "))
            hyp.append(ligne[2].split(" "))
    for i in range(len(ref)):
        if len(ref[i]) == len(hyp[i]):
            for j in range(len(ref[i])):
                r = ref[i][j]
                h = hyp[i][j]
                if r != "<eps>" and h != "<eps>" and r != h:
                    substitutions.append((r, h))

    def most_frequent(List, n):
        occurence_count = Counter(List)
        return occurence_count.most_common(n)

    fresults.write("Top confusion pairs: " + str(most_frequent(substitutions, n=10)) + "\n")


"""--------------exp14-substitutions-confusion-matrix-------------------------"""
if 14 in launch_expes:
    pos_refs = []
    pos_hyps = []
    errs = [] #[['=','D','=','D'], ['=', '='], [...]...]
    with open("data/" + args.id + "/" + args.id + "6.txt", "r", encoding="utf8") as file:
        for ligne in file:
            errs.append(ligne.split("\t")[2].split(" "))
    with open("data/" + args.id + "/" + args.id + "4.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne.split("\t")
            pos_refs.append(ligne[1].split(" "))
            pos_hyps.append(ligne[2].split(" "))
    if len(pos_refs) != len(pos_hyps) and len(pos_hyps) != len(errs):
        print("Erreur: pos_refs et pos_hyps et errs n'ont pas la même longueur")
        exit(-1)
    sub_conf_mat = dict()
    for p in POS_possible:
        sub_conf_mat[mapper[p]] = []
    counter = 0
    counter2=0
    for i in range(len(pos_hyps)):
        if len(errs[i]) != len(pos_hyps[i]) or len(errs[i]) != len(pos_refs[i]):
            counter += 1
            """print("Erreur: pos_refs[" + str(i) + "] et pos_hyps[" + str(i) + "] et errs[" + str(i) + "] n'ont pas la même longueur")
            print("len(pos_refs[i]) = " + str(len(pos_refs[i])))
            print("len(pos_hyps[i]) = " + str(len(pos_hyps[i])))
            print("len(errs[i]) = " + str(len(errs[i])))"""
        else:
            counter2+=1
            for j in range(len(errs[i])):
                if errs[i][j] == 'S':
                    if pos_hyps[i][j] != "<eps>" and pos_refs[i][j] != "<eps>":
                        if mapper[pos_refs[i][j]] in sub_conf_mat:
                            sub_conf_mat[mapper[pos_refs[i][j]]].append(mapper[pos_hyps[i][j]])

    old = POS_possible
    POS_possible = POS_possible2
    matrix = []
    i = 0
    keys = list(sub_conf_mat.keys())
    keys.sort()
    #for k, v in sub_conf_mat.items():
    for k in keys:
        v = sub_conf_mat[k]
        row = []
        if k != POS_possible[i]:
            print(POS_possible)
            print(sub_conf_mat.keys())
            print(k)
            fresults.write("ERREUR lors de l'expérience 2.\n")
            exit(-1)
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
    plt.savefig("results/Sub_confusion_matrix_percent_" + args.id + ".png")
    #fresults.write("La POS confusion matrix de " + args.id + " a été enregistré dans /results.\n")
    POS_possible = old



"""--------------exp15-character-error-rate---------------------"""
if 15 in launch_expes:
    from jiwer import cer
    refs = []
    hyps = []
    with open("data/" + args.id + "/" + args.id + "1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne.split("\t")
            ref = retirerEPS(ligne[1])
            hyp = retirerEPS(ligne[2])
            refs.append(ref)
            hyps.append(hyp)
    error = cer(refs, hyps)
    fresults.write("Character Error Rate: " + str(error) + "\n")




fresults.close()
