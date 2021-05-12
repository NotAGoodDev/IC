#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import os



##### PRUEBAS #####

# X = np.array([
#     [3, 5],
#     [5, 5],
#     [4, 5],
#     [3, 1],
#     [1, 3],
#     [2, 2],
#     [1, 1],
#     [2, 3],
#     [0, 2],
# ])

# Y = np.array([
#     'C1',
#     'C1',
#     'C1',
#     'C2',
#     'C2',
#     'C2',
#     'C3',
#     'C3',
#     'C3',
# ])

# vName = ['C1', 'C2', 'C3']

##### PRUEBAS #####



def obtenerMedias(X, Y, vName):
    medias = []
    for name in vName:
        pos = np.where(Y == name)
        medias.append(np.mean(X[pos], axis=0))

    return np.array(medias)



def covariante(X, media):
    return X - media



def obtenerCovariantes(X, Y, vName, medias):
    res = []
    for i in range(len(vName)):
        posX = np.where(Y == vName[i])            # Conocer las posiciones
        aux = covariante(X[posX], medias[i])      # Calcular covariantes
        nDatos = posX[0].shape[0]                 # Numero de datos
        
        acumulado = np.zeros((aux.shape[1], aux.shape[1])) # Acumulado
        
        for j in range(aux.shape[0]):
            value = np.array([aux[j]])                     # (i,) -> (i, 1)
            acumulado += (1 / nDatos) * (value * value.T)  # (1/n) * (v*v.T)
            
        res.append(acumulado) # Guardamos en un array los acumulados
        
    return np.array(res)



def pertenenciaBayes(X, medias, vName):
    
    distancias = []
    for i in range(medias.shape[0]):
        aux = np.array([X - medias[i]])
        I = np.identity(aux.shape[1])
        distancias.append(np.sum(aux * I * aux.T))
    
    return np.argmin(np.array(distancias))



def testBayes(medias, vName):
    print("########## TEST DE BAYES ##########")
    for file in os.listdir('test'):
        df = pd.read_csv('test/' + file, header=None)
        pruebaX = np.array(df.iloc[:, :-1])
        pruebaY = np.array(df.iloc[:, -1])
        posMin = pertenenciaBayes(pruebaX, medias, vName)

        print("El archivo {} pertenece a la clase \n{}\n"
             .format(file, vName[posMin]))



def bayes(X, Y, vName):
    medias = obtenerMedias(X, Y, vName)
    covariantes = obtenerCovariantes(X, Y, vName, medias)
    print("\n########## ENTRENAMIENTO DE BAYES ##########\n")
    print("Las covariantes obtenidas son: \n{}\n"
          .format(covariantes))
    return medias

