from flair.data import Sentence
from flair.models import SequenceTagger




# load tagger
tagger = SequenceTagger.load("flair/upos-multi")#-fast") #MODIFICATION

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

    #sentence : "JE SUIS <eps> CONTENT"
    #sentence : "JE SUIS CONTENT"
    #pos : "PRON VERB ADJ"
    #pos : "PRON VERB <eps>

    #Ce qui pourrait être utile serait de créer une fausse POS appelé <eps> car il est possible que la catégorie "X" pour "other" soit utile.
    #Si je fais ça, il faut que je modifie la variable POS
    #C'est une question que je peux effectivement poser à Mickael : comment prendre en compte ces bloc ?

    return pos



def cleanString(line):
    """
    Input : 
        line = "BONJOUR   ;   JE  ; VAIS  ; BIEN"
    Ouput :
        line = "BONJOUR JE VAIS BIEN"
    """
    line = line.split()
    line = "".join(str(x) for x in line)
    line = line.split(";")
    line = " ".join(str(x) for x in line)
    return line



#namefile = "temp2.txt"
namefile = "wer_test.txt"
namenew = "POS_analysis.txt"





f = open(namefile, "r", encoding="utf8")
nf= open(namenew, "w", encoding="utf8")


"""----------------ATTENTION AU SOUCI QUE VA APPORTER LES <eps>-------------"""


POS_stats = {"ADJ":{"S":0, "I":0, "D":0, "=":0},"ADP":{"S":0, "I":0, "D":0, "=":0},"ADV":{"S":0, "I":0, "D":0, "=":0},"AUX":{"S":0, "I":0, "D":0, "=":0},"CCONJ":{"S":0, "I":0, "D":0, "=":0},"DET":{"S":0, "I":0, "D":0, "=":0},"INTJ":{"S":0, "I":0, "D":0, "=":0},"NOUN":{"S":0, "I":0, "D":0, "=":0},"NUM":{"S":0, "I":0, "D":0, "=":0},"PART":{"S":0, "I":0, "D":0, "=":0},"PRON":{"S":0, "I":0, "D":0, "=":0},"PROPN":{"S":0, "I":0, "D":0, "=":0},"PUNCT":{"S":0, "I":0, "D":0, "=":0},"SCONJ":{"S":0, "I":0, "D":0, "=":0},"SYM":{"S":0, "I":0, "D":0, "=":0},"VERB":{"S":0, "I":0, "D":0, "=":0},"X":{"S":0, "I":0, "D":0, "=":0}, "<eps>":{"S":0, "I":0, "D":0, "=":0}}
#The monster above mean that we want to know the number of errors for each POS
#POS["ADJ"]["S"] = 5 #this mean that in our corpus, the adjectives were substitute by another word 5 times.

def analysis(pos, correction):
    pos = pos.split(" ")
    correction = correction.split(" ")
    if len(pos) != len(correction):
        print(pos)
        print(correction)
        print("Error: length of 'pos' and 'correction' is not the same")
        exit(-1)
    for i in range(len(pos)):
        POS_stats[pos[i]][correction[i]] += 1 #NE MARCHERA PAS A CAUSE DES <eps>


lines = f.readlines()[12:]
i = 0
while i < len(lines):
    print(i)
    i += 1
    line1 = cleanString(lines[i])
    i += 1
    correction = cleanString(lines[i]) #" I ; S ; = ; = ; D " ---> "I S = = D"
    i += 1
    line2 = cleanString(lines[i])
    i += 2

    #print(line1)
    #print(correction)
    pos1 = POS(line1)
    print(line1)
    #print(pos1)
    analysis(pos1, correction)

nf.write(str(POS_stats) + "\n")

f.close()
nf.close()

