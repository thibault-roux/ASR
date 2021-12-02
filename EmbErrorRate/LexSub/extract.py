#'lexsub_fr.xml'


import xml.etree.ElementTree as et


liste = []
with open("gold_fr.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split(" ::")[1]
        ligne = ligne.split(";")
        l = ""
        for i in range(len(ligne) - 1):
            l += (ligne[i][1:-2]) + ";"
        liste.append(l[:-1])




my_tree = et.parse('lexsub_fr.xml')
my_root = my_tree.getroot()

txt = ""
ind = 0
for index in range(len(my_root)):
    #print(my_root[index][0].attrib)
    for a in my_root[index]:
        for e in a:
            for i in e.itertext():
                txt += i + "\t"
            txt += liste[ind] + "\n"#liste de mot pouvant remplacer séparé par des ";"
        ind += 1

print(txt.count("\n"))


with open("lexsub.txt", "w", encoding="utf8") as file:
    file.write(txt)
