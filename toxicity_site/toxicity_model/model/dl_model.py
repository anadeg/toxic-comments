import os

import numpy as np
import pandas as pd
import re
import string
import tensorflow
from keras import Sequential
from keras.layers import GlobalAveragePooling1D
from keras.layers.core import Embedding, Dense, Dropout
from sklearn.model_selection import train_test_split


DIR_NAME = os.path.dirname(os.path.abspath(__file__))
train = pd.read_csv(os.path.join(DIR_NAME, "comments.csv"))

embedding_dim = 16
max_features = 10000
sequence_length = 250


def custom_standardization(sentence):
    sample = tensorflow.strings.lower(sentence)
    sample = tensorflow.strings.regex_replace(sample, '\W', ' ')
    sample = tensorflow.strings.regex_replace(sample, '\d', ' ')
    return tensorflow.strings.regex_replace(sample, '[%s]'%re.escape(string.punctuation), '')


def fit_model():
    X = train["comment_text"]
    Y = train[train.columns[2:]]
    X = np.array(vectorize_layer(X))

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    cnn_epochs = 10
    cnn_model.fit(X_train, y_train, epochs=cnn_epochs, batch_size=512, validation_data=(X_test, y_test))


def predict_model(x):
    x = np.array([[x]])
    x = vectorize_layer(x)
    return cnn_model.predict(x)


vectorize_layer = tensorflow.keras.layers.TextVectorization(
                            standardize=custom_standardization,
                            split='whitespace',
                            max_tokens=max_features,
                            output_mode='int',
                            output_sequence_length=sequence_length,
                            encoding='utf-8')
vectorize_layer.adapt(train['comment_text'])

cnn_model = Sequential()
cnn_model.add(Embedding(max_features+1, embedding_dim))
cnn_model.add(Dropout(0.2))
cnn_model.add(GlobalAveragePooling1D())
cnn_model.add(Dropout(0.2))
cnn_model.add(Dense(16, activation='relu'))
cnn_model.add(Dense(6, activation='sigmoid'))
cnn_model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])


