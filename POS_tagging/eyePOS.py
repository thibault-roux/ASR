


with open("POS_analysis.txt", "r", encoding="utf8") as file:
    for ligne in file:
        txt = ligne
        break

exec("POS_stats = " + ligne)

error_type = ["S", "I", "D", "="]
for key_POS, val_POS in POS_stats.items():
    temp = []
    for key_error, val_error in val_POS.items():
        temp.append(val_error)
    total = sum(temp)
    if total > 100:
        print(key_POS + ",", end="")
        for i in range(len(temp)):
            try:
                percent = int(temp[i]/total*100)
            except ZeroDivisionError:
                percent = 0
            print(str(percent), end=",")
            #print(error_type[i] + " : " + str(percent), end= "%, ")
        print(total)
        #print("total = " + str(total))
