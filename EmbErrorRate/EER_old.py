import numpy as np

"""
UNE STRATEGIE QUE JE POURRAIS FAIRE:
    - Pour savoir comment estimer la valeur d'erreur quand le mot transcrit est différent
    du mot de référence, je pourrais regarder la distribution des distances de voisinage
    entre des synonymes dans l'espace d'embeddings que j'utiliserai.
    - Il faudra pour ça que je trouve un dataset avec des synonymes. WordNet a sûrement
    une API ou quelque chose de ce genre.



%WER 120.00 [ 6 / 5, 2 ins, 0 del, 4 sub ]
J ; AIMERAIS ; ENVOYER ;   UN   ; FAX ; <eps> ; <eps>
= ;    S     ;    S    ;   S    ;  S  ;   I   ;   I
J ;    AI    ;    L    ; AURAIS ;  EN ;  VOYA ; FAXCI

0 ;    n1    ;    n2   ;   n3   ;  n4 ;   1   ;   1
Est-ce que je dois mettre n_x entre 0 et 1 ?
Sachant que 1 est le meilleur score (en tant que voisin) et que plus ça tend
vers len(voc), moins c'est bon.


n_x     val
1       0
2
3
...
10000   0,999
"""




"""
Il serait intéressant de regarder la distance moyenne entre synonymes.
De cette manière, on pourrait décider si ces mots sont une erreur.
Cette page pourrait me servir : https://www.guru99.com/wordnet-nltk.html
Aussi, je pourrai utiliser la similarité cosinus plutôt que la distance de
voisinage
"""

#Lecture du fichier contenant les erreurs
sentences = []
errors = []
with open("../data/fra4.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        sentences.append(ligne[0])
        errors.append(ligne[1])


#Lecture des embeddings
embeddings = {}
#namefile = "../../../Stage/embeddings_fast_text/cc.fr.300.vec"
namefile = "../../../Stage/embeddings_fast_text/temp.vec"

vocab = {}
embeddings = []
with open(namefile, "r", encoding="utf8") as emb:
    next(emb)
    i = 0
    for ligne in emb:
        ligne = ligne.split(" ")
        vocab[ligne[0].lower()] = i
        embeddings.append(np.array(ligne[1:], dtype=np.float32))
        i += 1


def most_similar_index(word_src, word_trg, vocab, embs_norm):
    word_src = word_src.lower()
    word_trg = word_trg.lower()
    if word_src not in vocab:
        return None
    if word_trg not in vocab:
        return None
    word_src_emb = embs_norm[vocab[word_src]] #embs_norm[vocab[word_src] if word_src in vocab else vocab[word_src.lower()]]
    sims = np.dot(word_src_emb, np.transpose(embs_norm))
    inds = np.argsort(sims)[::-1]
    trg_ind = vocab[word_trg]
    return np.where(inds == trg_ind)[0][0] + 1

print(vocab)
tset = []
for k, v in vocab.items():
    tset.append(most_similar_index("coucou", k, vocab, embeddings))

ind = most_similar_index("coucou", "wesh", vocab, embeddings)
if ind:
    pass
else:
    pass #le mot n'a pas été trouvé
