from flair.data import Sentence
from flair.models import SequenceTagger
#tagger = SequenceTagger.load("flair/upos-multi") #-fast") #FAST FOR NOW

print("Loading Flair tagger...")
tagger = SequenceTagger.load("flair/upos-multi-fast") #MODIFICATION
print("Flair tagger loaded.")

# iterate over entities and print
def getPosTxt(sentence):
    """
    Input :
        sentence = #Format Sentence with associated POS
    Output :
        pos = "PRON VERB ADJ"
    """
    pos = ""
    temp = sentence.get_spans()
    for i in range(len(temp)):
        pos += temp[i].tag + " "
    pos = pos[:-1]
    return pos

def get_list_index(elem, l):
    return [i for i,d in enumerate(l) if d==elem]

def POS(sentence):
    """
    Input :
        sentence = "BONJOUR JE VAIS BIEN <eps> <eps>"
    Output :
        pos = #part-of-speech of sentence with <eps> symbol instead of pos
    """
    #The next part is useful to delete <eps> from the sentence but to keep it in memory
    sentence = sentence.split(" ")
    eps_index = get_list_index("<eps>", sentence)
    eps_index.sort(reverse=True)
    for ind in eps_index:
        del sentence[ind]
    sentence = " ".join(str(x) for x in sentence)

    #Prediction of POS
    sentence = Sentence(sentence)
    tagger.predict(sentence)
    pos = getPosTxt(sentence)

    #Adding <eps> in POS sentence
    pos = pos.split(" ")
    eps_index.sort()
    for ind in eps_index:
        pos.insert(ind, "<eps>")
    pos = " ".join(str(x) for x in pos)
    return pos



def tag(id):
    ref = []
    hyp = []
    with open("data/" + id + "1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ref.append(ligne.split("\t")[0])
            hyp.append(ligne.split("\t")[1])


    #Pour chaque POS de la réf, j'ajoute le POS de la transcription associé dans le dictionnaire ci-dessous
    POS_matrix = {"ADJ":[],"ADP":[],"ADV":[],"AUX":[],"CCONJ":[],"DET":[],"INTJ":[],"NOUN":[],"NUM":[],"PART":[],"PRON":[],"PROPN":[],"PUNCT":[],"SCONJ":[],"SYM":[],"VERB":[],"X":[], "<eps>":[]}

    POS_to_file = ""

    for i in range(len(ref)):
        print(i)
        r = POS(ref[i])
        h = POS(hyp[i])
        POS_to_file += r + "\t" + h + "\t_\n"
        #print(r)
        #print(h)
        r = r.split(" ")
        h = h.split(" ")
        if len(r) != len(h):
            print("Error: Different length between reference and hypothesis !")
            exit()
        for j in range(len(r)):
            POS_matrix[r[j]].append(h[j])

    with open("data/" + id + "4.txt", "w", encoding="utf8") as file:
        file.write(POS_to_file)

    import pickle

    pickle.dump(POS_matrix, open("pickle/POS_matrix" + id + ".pickle", "wb"))
