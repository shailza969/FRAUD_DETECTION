# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 12:45:30 2021

@author: hp
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from minisom import MiniSom

dataset = pd.read_csv('Credit_Card_Applications.csv')
X = dataset.iloc[:, :-1].values
Y = dataset.iloc[:, -1].values

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range= (0, 1))
X = sc.fit_transform(X)

som = MiniSom(x= 10, y= 10, input_len= 15, sigma= 1.0 )
som.random_weights_init(X)
som.train_random(data = X, num_iteration= 100)

from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map())
colorbar()
markers = ['o', 's']
colors = ['r', 'g']

for i, x in enumerate(X):
    w = som.winner(x)
    plot(w[0]+0.5, 
         w[1]+0.5,
         markers[Y[i]],
         markeredgecolor = colors[Y[i]],
         markerfacecolor = 'None',
         markersize = 10,
         markeredgewidth = 2)
show()



mappings = som.win_map(X)
frauds = np.concatenate((mappings[(3,1)], mappings[(4, 2)]), axis= 0)
frauds = sc.inverse_transform(frauds)

customers = dataset.iloc[:, 1:].values


is_fraud = np.zeros(len(dataset))
for i in range(len(dataset)):
    if dataset.iloc[i, 0] in frauds:
        is_fraud[i] = 1

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
customers = sc.fit_transform(customers)

import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

ann = Sequential()
ann.add(Dense(units = 2, activation = 'relu'))
ann.add(Dense(units=1, activation='sigmoid'))

ann.compile(optimizer = 'adam', loss= 'binary_crossentropy', metrics = ['accuracy'])

ann.fit(customers, is_fraud, epochs = 100, batch_size = 1)


y_pred = ann.predict(customers)
y_pred = np.concatenate((dataset.iloc[:, 0:1].values, y_pred), axis = 1)
y_pred = y_pred[y_pred[:, 1].argsort()]
