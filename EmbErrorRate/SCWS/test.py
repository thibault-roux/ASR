
ratings = []

with open("ratings.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        #print(len(ligne))
        #print(ligne[5]) #phrase 1
        #print(ligne[6]) #phrase 2
        #print(ligne[7]) #rating moyen
        ratings.append(float(ligne[7]))

print(len(ratings))
mean = sum(ratings)/len(ratings)
print(mean)
