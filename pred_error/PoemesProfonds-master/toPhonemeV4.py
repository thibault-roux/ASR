import preprocessing as pp
from lecture import *
from keras.models import load_model
import pandas as pd
import progressbar

import os
java_path = "C:/Program Files/Java/jdk1.8.0_251/bin/java.exe"
os.environ['JAVAHOME'] = java_path

dico_u, dico_m, df_w2p = pd.read_pickle(os.path.join(".", "data", "dicos.pickle"))
ltr2idx, phon2idx, Tx, Ty = pp.chars2idx(df_w2p)
model_lire = load_model(os.path.join(".", "models", "lecteur", "lecteur_mdl.h5")) #"CE1_T12_l10.h5"))
lecteur = Lecteur(Tx, Ty, ltr2idx, phon2idx, dico_u, dico_m, n_brnn1=90, n_h1=80, net=model_lire, blank="_")

print()
print(lecteur.lire_vers("Les trains arrivent en gare de Jarlitude, voies 14 et 97."))
print()

txt = ""
i = 0
bar = progressbar.ProgressBar(max_value=15659)
with open("../../data/fra8.txt", "r", encoding="utf8") as file:
    for ligne in file:
        #print(i)
        i += 1
        ligne = ligne.split("\t")
        ligne0 = ligne[0].split(" ")
        ligne1 = ligne[1].split(" ")

        ref = ""
        for j in range(len(ligne0)):
            if ligne0[j] != "<eps>":
                ref += ligne0[j] + " "
                #lecteur.lire_vers(ligne0[j]) + " "
        ref = ref[:-1]

        hyp = ""
        for j in range(len(ligne1)):
            if ligne1[j] != "<eps>":
                hyp += ligne1[j] + " "
        hyp = hyp[:-1]

        txt += lecteur.lire_vers(ref) + "\t" + lecteur.lire_vers(hyp) + "\t_\n"
        bar.update(i)

with open("../../data/fra13.txt", "w", encoding="utf8") as f:
    f.write(txt)
