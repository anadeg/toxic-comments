import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
import tensorflow
from keras import Sequential
from keras.layers import Embedding, GlobalAveragePooling1D, Dense

from sklearn.model_selection import train_test_split

# from tensorflow.keras import Sequential
# from tensorflow.keras.layers import *
# from tensorflow.keras.losses import *
# from tensorflow.keras.metrics import *
# from tensorflow.keras.optimizers import *


class ToxicityModel:
    data_file = "comments.csv"
    max_features = 10000
    sequence_length = 250
    embedding_dim = 9
    cnn_epochs = 5

    def __init__(self):
        self.data = pd.read_csv(self.data_file)
        self.X = self.data["comment_text"]
        self.Y = self.data[self.data.columns[2:]]
        self.cnn_model = None

    def vectorize(self, x):
        vectorize_layer = tensorflow.keras.layers.TextVectorization(
            standardize=self.custom_standardization,
            split='whitespace',
            max_tokens=self.max_features,
            output_mode='int',
            output_sequence_length=self.sequence_length,
            encoding='utf-8')
        vectorize_layer.adapt(self.data['comment_text'])

        return np.array(vectorize_layer(x))

    def fit(self):
        self.X = self.vectorize(self.X)

        self.cnn_model = Sequential()
        self.cnn_model.add(Embedding(self.max_features + 1, self.embedding_dim))
        self.cnn_model.add(GlobalAveragePooling1D())
        self.cnn_model.add(Dense(16, activation='relu'))
        self.cnn_model.add(Dense(6, activation='sigmoid'))

        self.cnn_model.compile(loss='binary_crossentropy',
                          optimizer='Adam',
                          metrics=['accuracy'])

        history = self.cnn_model.fit(self.X,
                                     self.Y,
                                     epochs=self.cnn_epochs,
                                     batch_size=512)

    def predict(self, x):
        x = self.vectorize(x)

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
        to_test = input()
    # to_test = "FUCK YOUR FILTHY MOTHER IN THE ASS, DRY!"

        result = tm.predict(np.array([to_test]).reshape(1, -1))
        print(result)
