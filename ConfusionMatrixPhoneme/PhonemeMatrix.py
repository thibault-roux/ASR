from wer import cer
import pickle


r, h, list, result = cer("Aviation", "Avitione")
print(r)
print(h)

phons = "<eps> k p l t R f s d Z n b v g m z S N G x a E § j o O i 1 5 e u @ ° 9 w y 8 2".split(" ")
matrix = dict()
for p in phons:
    matrix[p] = dict()
    for p_ in phons:
        matrix[p][p_] = 0


ref = []
hyp = []
with open("../data/fra13_incompleted.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        ref.append(ligne[0])
        hyp.append(ligne[1])

for i in range(len(ref)):
    if i%500 == 0:
        print(i)
    try:
        r, h, list, result = cer(ref[i], hyp[i])
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

for k, v in matrix.items():
    if v != []:
        print(k, v)

pickle.dump(matrix, open("matrix.pickle", "wb"))
#print(matrix)
