import preprocessing as pp
from lecture import *
from keras.models import load_model
import pandas as pd

import os
java_path = "C:/Program Files/Java/jdk1.8.0_251/bin/java.exe"
os.environ['JAVAHOME'] = java_path

dico_u, dico_m, df_w2p = pd.read_pickle(os.path.join(".", "data", "dicos.pickle"))
ltr2idx, phon2idx, Tx, Ty = pp.chars2idx(df_w2p)
model_lire = load_model(os.path.join(".", "models", "lecteur", "lecteur_mdl.h5")) #"CE1_T12_l10.h5"))
lecteur = Lecteur(Tx, Ty, ltr2idx, phon2idx, dico_u, dico_m, n_brnn1=90, n_h1=80, net=model_lire, blank="_")

#lecteur.lire_vers("Les trains arrivent en gare de Jarlitude, voies 14 et 97.")

txt = ""
i = 0
with open("../../data/fra8_temp.txt", "r", encoding="utf8") as file:
    for ligne in file:
        print(i)
        i += 1
        ligne = ligne.split("\t")
        ligne0 = ligne[0].split(" ")
        ligne1 = ligne[1].split(" ")
        for j in range(len(ligne0)):
            if ligne0[j] != "<eps>":
                txt += lecteur.lire_vers(ligne0[j]) + " "
            else:
                txt += "<eps> "
        txt = txt[:-1] + "\t"
        for j in range(len(ligne1)):
            if ligne1[j] != "<eps>":
                txt += lecteur.lire_vers(ligne0[j]) + " "
            else:
                txt += "<eps> "
        txt = txt[:-1] + "\t_\n"
        #txt += lecteur.lire_vers(ligne[0]) + "\t" + lecteur.lire_vers(ligne[1]) + "\t_\n"

with open("../../data/fra10.txt", "w", encoding="utf8") as f:
    f.write(txt)
