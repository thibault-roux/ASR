
correct = 0
total = 0
namefile="repere_wer.txt"
#namefile="wer_test.txt"
#namefile="wer_postSP2.txt"
with open(namefile, "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split(" ")
        if len(ligne) > 4:
            if ligne[1] == "%WER":
                correct += int(ligne[4])
                total += int(ligne[6][:-1])

print("WER:", end=" ")
a = "{:.2f}".format(float(correct/total)*100)
print(a)
