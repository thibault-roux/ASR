with open("lexsub.txt", "r", encoding="utf8") as file:
    for ligne in file:
        print(ligne.split("\t")[3])
        exit()


"""
liste = []

with open("gold_fr.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split(" ::")[1]
        ligne = ligne.split(";")
        l = ""
        for i in range(len(ligne) - 1):
            l += (ligne[i][1:-2]) + ";"
        liste.append(l[:-1])

print(liste[0])
print(liste[1])
"""
