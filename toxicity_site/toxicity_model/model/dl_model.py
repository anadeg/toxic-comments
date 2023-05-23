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

from tensorflow import keras

DIR_NAME = os.path.dirname(os.path.abspath(__file__))


class ToxicityModel:
    data_file = os.path.join(DIR_NAME, "comments.csv")
    max_features = 20000
    sequence_length = 250
    # sequence_length = 150
    embedding_dim = 16
    # cnn_epochs = 5
    cnn_epochs = 2

    def __init__(self):
        # id,comment_text
        # toxic, severe_toxic, obscene, threat, insult, identity_hate
        self.data = pd.read_csv(self.data_file,
                                dtype={"id": "category",
                                       # "comment_text": "category",
                                       "toxic": "int8",
                                       "severe_toxic": "int8",
                                       "obscene": "int8",
                                       "threat": "int8",
                                       "insult": "int8",
                                       "identity_hate": "int8"},
                                encoding='utf-8')
        self.X = self.data["comment_text"]
        self.Y = self.data[self.data.columns[2:]]

        self.cnn_model = Sequential()
        self.cnn_model.add(Embedding(self.max_features + 1,
                                     self.embedding_dim,
                                     embeddings_regularizer=keras.regularizers.l1_l2()))
        # self.cnn_model.add(Dropout(0.2))
        self.cnn_model.add(GlobalAveragePooling1D())
        # self.cnn_model.add(Dropout(0.2))
        self.cnn_model.add(Dense(16, activation='relu', kernel_regularizer=keras.regularizers.l1_l2()))
        self.cnn_model.add(Dense(6, activation='sigmoid', kernel_regularizer=keras.regularizers.l1_l2()))

        self.cnn_model.compile(loss='binary_crossentropy',
                               optimizer='Adam',
                               metrics=['accuracy'])

        self.vectorize_layer = tensorflow.keras.layers.TextVectorization(
            standardize=self.custom_standardization,
            split='whitespace',
            max_tokens=self.max_features,
            output_mode='int',
            output_sequence_length=self.sequence_length,
            encoding='utf-8')
        self.vectorize_layer.adapt(self.X)

    def vectorize(self, x):
        return np.array(self.vectorize_layer(x))

    def fit(self):
        self.X = self.vectorize(self.X)
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.2)
        self.cnn_model.fit(X_train,
                           y_train,
                           epochs=self.cnn_epochs,
                           batch_size=256,
                           validation_data=(X_test, y_test))

    def predict(self, x):
        x = np.array([x]).reshape(1, -1)
        x = self.vectorize(x)

        # print(x)

        cnn_prediction = self.cnn_model.predict(x)
        return cnn_prediction

    @staticmethod
    def custom_standardization(sentence):
        sample = tensorflow.strings.lower(sentence)
        sample = tensorflow.strings.regex_replace(sample, '\W', ' ')
        sample = tensorflow.strings.regex_replace(sample, '\d', ' ')
        return tensorflow.strings.regex_replace(sample, '[%s]' % re.escape(string.punctuation), '')


if __name__ == "__main__":
    tm = ToxicityModel()
    tm.fit()
    while True:
        print("=============================")
        to_test = input()
    # to_test = "FUCK YOUR FILTHY MOTHER IN THE ASS, DRY!"

        result = tm.predict(to_test)
        print(result)
