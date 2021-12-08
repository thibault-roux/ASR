#from POS_tag import tag

import argparse
parser = argparse.ArgumentParser(description="Create dataset")
parser.add_argument("namef", type=str, help="Path to a test file output")
parser.add_argument("id", type=str, help="ID (SP, KD, etc...)")
args = parser.parse_args()


"""
Logs file without buffering for instant output
"""
bufsize = 0
logf = open("log.txt", "w", buffering=1, encoding="utf8")
def prin(txt):
    logf.write(txt + "\n")



def clean(line):
    line = line.split(";")
    line = " ".join(line)
    """line = line.split("<eps>")
    line = " ".join(line)"""
    line = line.split()
    line = " ".join(line)
    return line




"""---------------SP1/KD1---------------"""
prin("Creation of " + args.id + "1...")
with open(args.namef, "r", encoding="utf8") as basefile:
    lines = basefile.readlines()
    X = ""
    i = 0
    while i < len(lines):
        i += 1
        line = clean(lines[i])
        X += line + "\t"
        i += 2
        line = clean(lines[i])
        X += line + "\t_\n"
        i += 2
with open("data/" + args.id + "1.txt", "w", encoding="utf8") as file:
    file.write(X)


"""---------------SP2/KD2---------------"""
prin("Creation of " + args.id + "2...")
with open(args.namef, "r", encoding="utf8") as basefile:
    lines = basefile.readlines()
    X = ""
    i = 0
    while i < len(lines):
        i += 1
        line = clean(lines[i])
        X += line + "\t"
        i += 1
        line = clean(lines[i])
        X += line + "\t_\n"
        i += 3
with open("data/" + args.id + "2.txt", "w", encoding="utf8") as file:
    file.write(X)


"""---------------SP3/KD3---------------"""
prin("Creation of " + args.id + "3...")
f = open("data/" + args.id + "2.txt", "r", encoding="utf8")
txt = ""
nbrErreur = 0
nbrLine = 0
for ligne in f:
    nbrLine += 1
    ligne = ligne.split("\t")
    errors = ligne[1].split(" ")
    Erreur = 0
    for e in errors:
        if e != "=":
            Erreur += 1
    if Erreur != 0:
        nbrErreur += 1
    txt += ligne[0] + "\t" + str(Erreur) + "\t_\n"
with open("data/" + args.id + "3.txt", "w", encoding="utf8") as file:
    file.write(txt)


"""---------------SP4/KD4---------------"""
prin("Creation of " + args.id + "4...")
#tag(args.id)
"""OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO       A REMETTRE     OOOOOOOOOOOOOOOOOOOOOOOOO"""


"""---------------SP5/KD5---------------"""
prin("Creation of " + args.id + "5...")
fpos = open("data/" + args.id + "4.txt", "r", encoding="utf8")
fbase= open("data/" + args.id + "1.txt", "r", encoding="utf8")
rpos = fpos.readlines()
rbase= fbase.readlines()
txt = ""
for i in range(len(rpos)):
    txt += rpos[i].split("\t")[0] + "\t" + rbase[i].split("\t")[0] + "\t" + rbase[i].split("\t")[1] + "\t_\n"
with open("data/" + args.id + "5.txt", "w", encoding="utf8") as file:
    file.write(txt)


"""---------------SP6/KD6---------------"""
prin("Creation of " + args.id + "6...")
fpos = open("data/" + args.id + "4.txt", "r", encoding="utf8")
ferr = open("data/" + args.id + "2.txt", "r", encoding="utf8")
rpos = fpos.readlines()
rerr = ferr.readlines()
txt = ""
for i in range(len(rpos)):
    txt += rpos[i].split("\t")[0] + "\t" + rerr[i].split("\t")[1] + "\t_\n"
with open("data/" + args.id + "6.txt", "w", encoding="utf8") as file:
    file.write(txt)

"""---------------SP7/KD7---------------"""
prin("Creation of " + args.id + "7...")


"""
------------------ATTENTION------------------

Je dois vérifier si je retire bien les epsilon pour
les expes concernés
---------------------------------------------
"""


prin("Fermeture du fichier de log.")
logf.close()
