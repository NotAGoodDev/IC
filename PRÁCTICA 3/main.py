#!/usr/bin/env python
# coding: utf-8


from Kmedias import *
from Bayes import *
from Lloyd import *


##### VARIABLES #####

df = pd.read_csv('entrenamiento.txt', header=None)

X = np.array(df.iloc[:, :-1])
Y = np.array(df.iloc[:, -1])

V = np.array([[4.5, 3.0, 4.0, 0.0], [6.8, 3.4, 4.6, 0.7]])
vName = np.unique(Y)

# K MEDIAS
b = 2
epsilonKmedias = 0.02

# BAYES -> NADA

# LLOYD
epsilonLloyd = 10**-10
kMax = 10
gamma = .1

##### VARIABLES #####


V_KMedias = kMedias(X, V, b, epsilonKmedias)
testKMedias(V_KMedias, vName)



medias = bayes(X, Y, vName)
testBayes(medias, vName)


vLloyd = lloyd(X, V, gamma, kMax, epsilonLloyd)
testLloyd(vLloyd, vName)

