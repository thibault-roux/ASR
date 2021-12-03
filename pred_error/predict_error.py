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
Seq2seq on word
"""

X = []
y = []
with open("fra5.txt", "r", encoding="utf8") as file:
    for ligne in file:
        ligne = ligne.split("\t")
        X.append(ligne[0])
        y.append(int(ligne[1]))

"""
print(y.count(0))
print(y.count(1))
print(len(y))
exit()"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
y_train = np.array(y_train)
y_test = np.array(y_test)


vocabulary = {"<OOV>": 0}
index = 1
for i in range(len(X_train)):
    for word in X_train[i].split(" "):
        if word not in vocabulary:
            vocabulary[word] = index
            index += 1

def voc2index(X):
    print("Processing data... voc2index")
    X_ = []
    for i in range(len(X)):
        temp = []
        for word in X[i].split(" "):
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
max_review_length = 23
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
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, batch_size=10491)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

predictions = model.predict(X_test)
import pickle
print(predictions)
pickle.dump(predictions, open("pickle/predictions.pck", "wb"))

"""
#0.6591
model.save("pickle/model.keras")
pickle.dump(X_train, open("pickle/X_train.pck", "wb"))
pickle.dump(X_test, open("pickle/X_test.pck", "wb"))
pickle.dump(y_train, open("pickle/y_train.pck", "wb"))
pickle.dump(y_test, open("pickle/y_test.pck", "wb"))"""
