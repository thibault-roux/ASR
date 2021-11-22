"""Ce code a pour objectif de transformer le fichier fra4.txt
dans une forme "binaire", càd qu'il y a 0 s'il n'y a pas d'erreur
et 1 s'il y en a une."""

f = open("fra4.txt", "r", encoding="utf8")

#1 = il y a une erreur
#0 = il n'y a pas d'erreur, il n'y a que des égalités
#Je peux refaire l'expe en essayant de prédire le nombre d'erreur

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
            Erreur = 1
    if Erreur != 0:
        nbrErreur += 1
    txt += ligne[0] + "\t" + str(Erreur) + "\t_\n"

print(nbrErreur)
print(nbrLine)

"""
with open("fra5.txt", "w", encoding="utf8") as file:
    file.write(txt)
"""
#print(nbrErreur/nbrLine*100) #Il y a 65% de phrase avec une erreur (SER)
