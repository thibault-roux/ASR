from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
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
Utiliser comme input les caractères (n==1)
Ou des n-grams de caractères (n>1)

Par exemple, la phrase "bonjour ça va ?" -> "bo", "on", "nj", "jo", etc

-> Mes expériences n'ont pas donné de résultats satisfaisant.
Le meilleur score que j'ai obtenu était 67,53% d'accuracy sachant qu'il
y a 64,91% de 1 dans le dataset. Cela peut être dû au split du dataset qui
contenait plus de 1 que prévu et que le modèle prédit une majorité de 1.

Avec les phonèmes, il n'y a pas de progrès notables.
Il serait intéressant de reessayer mais en prédisant le nombre d'erreur
plutôt que une valeur binaire
"""

X = []
y = []
with open("../data/fra6.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        X.append(ligne[0])
        y.append(int(ligne[1]))

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

X_train = voc2index(X_train) #from text to index
X_test = voc2index(X_test)

#truncate and pad input sequences
max_review_length = 130 #23 #130
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

#replace top_word
input_dim = len(vocabulary)

# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(input_dim, embedding_vecor_length, input_length=max_review_length))
model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(100)))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=807) #10491

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

import pickle
#0.6591
model.save("pickle/model.keras")
pickle.dump(X_train, open("pickle/X_train.pck", "wb"))
pickle.dump(X_test, open("pickle/X_test.pck", "wb"))
pickle.dump(y_train, open("pickle/y_train.pck", "wb"))
pickle.dump(y_test, open("pickle/y_test.pck", "wb"))
