

f = open("pretransform.txt", "r", encoding="utf8")
nf1=open("fra8.txt", "w", encoding="utf8")
#nf2=open("Y.txt", "w", encoding="utf8")

X = ""
#Y = ""


"""Modifier le code pour prédire les substitutions, deletions, etc"""



def clean(line):
    line = line.split(";")
    line = " ".join(line)
    """line = line.split("<eps>")
    line = " ".join(line)"""
    line = line.split()
    line = " ".join(line)
    return line


lines = f.readlines()
i = 0
while i < len(lines):
    i += 1
    line = clean(lines[i])
    X += line + "\t"
    i += 2
    line = clean(lines[i])
    X += line + "\t_\n"
    i += 2

nf1.write(X)
#nf2.write(Y)

f.close()
nf1.close()
#nf2.close()
