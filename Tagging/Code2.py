# -*- coding: utf-8 -*-
"""Welcome To Colaboratory

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb
"""

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import string
import pandas as pd
import numpy as np
import re
import nltk
import spacy
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# Load the CSV file
df = pd.read_csv('/content/Tag_dataset.csv')

# Data Cleaning
df.dropna(subset=['Description'], inplace=True)  # Drop rows with missing descriptions
df.drop_duplicates(subset=['Description'], keep='first', inplace=True)  # Remove duplicates

# Text Preprocessing with Lemmatization and Stopword Removal
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def lemmatize_text(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(lemmatized_tokens)

df['lemmatized_description'] = df['Description'].apply(lemmatize_text)

# Remove Stopwords from Lemmatized Text
def remove_stopwords(text):
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    return ' '.join(filtered_tokens)

df['cleaned_lemmatized_description'] = df['lemmatized_description'].apply(remove_stopwords)

# Create Array of Words from Cleaned Lemmatized Description
def create_word_array(text):
    return word_tokenize(text)

df['word_array'] = df['cleaned_lemmatized_description'].apply(create_word_array)

# Perform POS Tagging on Each Word in Each Array
def pos_tag_words(word_array):
    return pos_tag(word_array)

df['pos_tagged_words'] = df['word_array'].apply(pos_tag_words)

# Create Separate Columns for Specific POS Tags
def extract_pos_tags(tagged_words, pos_tag):
    return ' '.join([word for word, tag in tagged_words if tag == pos_tag])

df['Nouns'] = df['pos_tagged_words'].apply(lambda x: extract_pos_tags(x, 'NN') + ' ' + extract_pos_tags(x, 'NNS') + ' ' + extract_pos_tags(x, 'NNP') + ' ' + extract_pos_tags(x, 'NNPS'))
df['Verbs'] = df['pos_tagged_words'].apply(lambda x: extract_pos_tags(x, 'VB') + ' ' + extract_pos_tags(x, 'VBD') + ' ' + extract_pos_tags(x, 'VBG') + ' ' + extract_pos_tags(x, 'VBN') + ' ' + extract_pos_tags(x, 'VBP') + ' ' + extract_pos_tags(x, 'VBZ'))
df['Adjectives'] = df['pos_tagged_words'].apply(lambda x: extract_pos_tags(x, 'JJ'))
# Save the preprocessed data with specific POS tagged words to a new CSV file
df.to_csv('Final_pd.csv', index=False)

import tensorflow as tf
from tensorflow import keras

df.head()

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['cleaned_lemmatized_description'])
# check unique words count
len(tokenizer.word_index)

# check unique words count
vocab_size = len(tokenizer.word_index) + 1
vocab_size

sequences = tokenizer.texts_to_sequences(df['cleaned_lemmatized_description'])
i = 0
print(df['cleaned_lemmatized_description'][i], '\n'), print(sequences[i])

seq_lengths = []

for i in sequences:
    seq_lengths.append(len(i))
print("30th percentile: ", pd.Series(seq_lengths).quantile(0.3))
print("40th percentile: ", pd.Series(seq_lengths).quantile(0.4))
print("50th percentile: ", pd.Series(seq_lengths).quantile(0.5))
print("60th percentile: ", pd.Series(seq_lengths).quantile(0.6))
print("70th percentile: ", pd.Series(seq_lengths).quantile(0.7))
print("80th percentile: ", pd.Series(seq_lengths).quantile(0.8))
print("90th percentile: ", pd.Series(seq_lengths).quantile(0.9))
print("95th percentile: ", pd.Series(seq_lengths).quantile(0.95))
print("99th percentile: ", pd.Series(seq_lengths).quantile(0.99))

max_length = 22

# padding
padded_seq = pad_sequences(sequences, maxlen=max_length)
from sklearn.preprocessing import MultiLabelBinarizer

multilabel_binarizer = MultiLabelBinarizer()
multilabel_binarizer.fit(df['Tags'])
y = multilabel_binarizer.transform(df['Tags'])
padded_seq.shape, y.shape

pip install tensorflow

from scikeras.wrappers import KerasClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Define a simple Keras model
def create_model():
    model = Sequential()
    model.add(Dense(10, input_dim=8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Create a KerasClassifier using scikeras
keras_model = KerasClassifier(build_fn=create_model, epochs=10, batch_size=32)

# Use the KerasClassifier in your scikit-learn workflow
# For example, you can use it in a scikit-learn Pipeline or GridSearchCV

from sklearn.model_selection import train_test_split

x_train, x_val, y_train, y_val = train_test_split(padded_seq, y,
                                                    test_size=0.1,
                                                    random_state=9)
from keras.models import Sequential, load_model
from keras.layers import Dense, Embedding, GlobalMaxPool1D, Dropout, Conv1D
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import GridSearchCV
from scikeras.wrappers import KerasClassifier

model = Sequential()
model.add(Embedding(vocab_size +1, 128, input_length = max_length))
model.add(Dropout(0.15))
model.add(Conv1D(300, 5, padding = 'valid', activation = "relu", strides = 1))
model.add(GlobalMaxPool1D())
model.add(Dense(100, activation = "sigmoid"))
#model.add(Activation('sigmoid'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()
tf.keras.layers.Flatten()

callbacks = [
             EarlyStopping(patience=3),
             ModelCheckpoint(filepath='model-conv1d_v1.h5', save_best_only=True)
            ]

history = model.fit(x_train, y_train,
                    epochs=15,
                    batch_size=64,
                    validation_split=0.1,
                    callbacks=callbacks)

preds = model.predict(x_val)

