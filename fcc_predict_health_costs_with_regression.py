# -*- coding: utf-8 -*-
"""fcc_predict_health_costs_with_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Cmc4q6Zuyiuqvh-tQBU5FZBWLGfJWb4
"""

!pip install -q git+https://github.com/tensorflow/docs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras 
from keras import layers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.layers import BatchNormalization
from keras.models import load_model
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
from sklearn.model_selection import train_test_split
from os import X_OK

# get data
!wget https://cdn.freecodecamp.org/project-data/health-costs/insurance.csv
dataset = pd.read_csv('insurance.csv')
dataset.head()

dataset.sex.loc[dataset.sex == 'male'] = 1
dataset.sex.loc[dataset.sex == 'female'] = 0
dataset.smoker.loc[dataset.smoker == 'yes'] = 1
dataset.smoker.loc[dataset.smoker == 'no'] = 0
dataset.region.loc[dataset.region == 'southeast'] = 0
dataset.region.loc[dataset.region == 'southwest'] = 1
dataset.region.loc[dataset.region == 'northwest'] = 3
dataset.region.loc[dataset.region == 'northeast'] = 4

X = dataset.iloc[ : , 0:6].values
y = dataset.expenses.values
y = y.astype('float32')
X = X.astype('float32')
train_dataset, test_dataset, train_labels, test_labels = train_test_split(X, y, test_size = 0.2)

tf.convert_to_tensor(train_dataset)
tf.convert_to_tensor(test_dataset)
tf.convert_to_tensor(train_labels)
tf.convert_to_tensor(test_labels)

model = Sequential() 
init = tf.keras.initializers.RandomUniform(minval=-0.05, maxval=0.05, seed=1)
model.add(Dense(32, activation = 'linear', kernel_initializer = init, input_shape = (6, )))
model.add(BatchNormalization())
model.add(Dense(16, activation = 'relu', kernel_initializer = init))
model.add(Dense(1, activation = 'linear'))
model.add(Dense(32, activation = 'linear', kernel_initializer = 'RandomNormal', input_shape = (6, )))
model.add(BatchNormalization())
model.add(Dense(16, activation = 'relu', kernel_initializer = 'RandomNormal'))
model.add(Dense(1, activation = 'linear'))
model.compile(optimizer = 'adam', loss = 'mse', metrics = 'mae')
es = EarlyStopping(monitor = 'mae', min_delta = 0, patience = 50, verbose = 0, mode = 'auto', baseline = None, restore_best_weights = True)
model.fit(train_dataset, train_labels, batch_size = 32, epochs = 400, validation_data = (test_dataset, test_labels), verbose = 1, callbacks = [es])

error = model.evaluate(test_dataset, test_labels, verbose = 1)

model.predict(test_dataset)
