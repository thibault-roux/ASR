from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import RobustScaler
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Bidirectional
from keras.layers import Dropout
from keras.layers.embeddings import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.preprocessing import sequence

"""
Variante de predict_error mais qui prédit le nombre d'erreur avec une régression

Utiliser comme input les caractères (n==1)
Ou des n-grams de caractères (n>1)

Par exemple, la phrase "bonjour ça va ?" -> "bo", "on", "nj", "jo", etc
"""

X = []
y = []
with open("../data/fra7.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        X.append(ligne[0])
        y.append(int(ligne[1]))

#scaler = RobustScaler() #NORMALISATION
#y = scaler.fit_transform(np.array(y).reshape(-1, 1))





"""Cette partie là sert à avoir une distribution assez uniforme"""
x = 6
for i in range(len(y)):
    if y[i] > x:
        y[i] = x

"""Cette partie là sert à avoir 523 éléments par 'classe' avec
0 à 6 les classes. Donc cela sert aussi à avoir une distribution uniforme.
"""
max = 523
counter = [523]*(x+1)
X_ = []
y_ = []
for i in range(len(X)):
    val = y[i]
    if counter[val] > 0:
        counter[val] -= 1
        X_.append(X[i])
        y_.append(y[i])

X = X_
y = y_







X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
y_train = np.array(y_train)
y_test = np.array(y_test)


def ngram_char(sentence, n):
    l = []
    for i in range(len(sentence)-(n-1)):
        l.append(sentence[i:i+n])
    return l

n = 1
vocabulary = {"<OOV>": 0} #vocabulaire de caractères
index = 1
for i in range(len(X_train)):
    #for word in X_train[i].split(" "):
    word = ngram_char(X_train[i], n)
    for c in word:
        if c not in vocabulary:
            vocabulary[c] = index
            index += 1

"""
print(len(vocabulary))
print(vocabulary)
exit()
"""

def voc2index(X):
    print("Processing data... voc2index")
    X_ = []
    for i in range(len(X)):
        temp = []
        #for word in X[i].split(" "):
        for word in ngram_char(X[i], n):
            try:
                ind = vocabulary[word]
            except KeyError:
                ind = vocabulary["<OOV>"]
            temp.append(ind)
        X_.append(temp.copy())
    return X_

def index2voc(sentIndex):
    sentVoc = ""
    for i in range(len(sentIndex)):
        for key, val in vocabulary.items():
            if val == sentIndex[i]:
                sentVoc += key
                break
    return sentVoc

"""
nbr = 0
for i in range(len(X_train)):
    if "V" in X_train[i]:
        y_train[i] = 1
        nbr += 1
    else:
        y_train[i] = 0
#print(nbr/len(X_train))
#exit()
for i in range(len(X_test)):
    if "V" in X_test[i]:
        y_test[i] = 1
    else:
        y_test[i] = 0
"""


X_train = voc2index(X_train) #from text to index
X_test = voc2index(X_test)


#truncate and pad input sequences
max_review_length = 130
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

#replace top_word
input_dim = len(vocabulary)

# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(input_dim, embedding_vecor_length, input_length=max_review_length))
#model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
#model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(100)))
model.add(Dropout(0.2))
model.add(Dense(1, activation='linear')) #'sigmoid'
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy']) #binary_crossentropy
print(model.summary())
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=807) #10491

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

from scipy import stats
pred = model.predict(X_test)
print(pred)
#for i in range(len(pred)):
#    print(pred[i], y_test[i])
print(stats.spearmanr(pred, y_test))

import pickle
#0.6591
model.save("pickle/model2.keras")
pickle.dump(X_train, open("pickle/X_train2.pck", "wb"))
pickle.dump(X_test, open("pickle/X_test2.pck", "wb"))
pickle.dump(y_train, open("pickle/y_train2.pck", "wb"))
pickle.dump(y_test, open("pickle/y_test2.pck", "wb"))
pickle.dump(pred, open("pickle/pred2.pck", "wb"))
