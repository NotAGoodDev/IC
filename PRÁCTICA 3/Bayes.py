#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import os



def obtenerMedias(X, Y, vName):
    """
    Calcula la media de los datos pertenecientes a una clase a partir de un conjunto de datos(X), sus respectivas clases(Y),
    y un array con el nombre de todas las clases.
    """
    
    medias = []
    for name in vName:
        pos = np.where(Y == name)
        medias.append(np.mean(X[pos], axis=0))

    return np.array(medias)



def covariante(X, media):
    """
    Calcula el covariante de un dato X[i] y su media
    """
    
    return X - media



def obtenerCovariantes(X, Y, vName, medias):
    """
    Calcula todas las covariantes a partir de un conjunto de datos(X), sus etiquetas(Y), un array
    con todas las etiquetas (vName) y las medias de dichas etiquetas/clases
    Devuelve un array con las covariantes
    """
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



def pertenenciaBayes(X, medias):
    """
    Devuelve la posición (en el array) de la distancia más cercana respecto a una media (centroide) a partir
    de un conjunto de datos (X) y la media de las clases (medias)
    """
    distancias = []
    for i in range(medias.shape[0]):
        aux = np.array([X - medias[i]])
        I = np.identity(aux.shape[1])
        distancias.append(np.sum(aux * I * aux.T))
    
    return np.argmin(np.array(distancias))



def bayes(X, Y, vName):
    """
    Gestiona el algoritmo de Bayes y devuelve las medias (centroides) a partir de
    un conjunto de datos X, su valor Y, y el nombre de todas las etiquetas (vName)
    """
    medias = obtenerMedias(X, Y, vName)
    covariantes = obtenerCovariantes(X, Y, vName, medias)
    print("\n########## ENTRENAMIENTO DE BAYES ##########\n")
    print("Las covariantes obtenidas son: \n{}\n"
          .format(covariantes))
    return medias



def testBayes(medias, vName, directorio='test'):
    """
    Función que calcula la distancia de todas las pruebas ubicadas en la carpeta test a partir del
    vector de medias y su etiqueta.
    No devuelve nada, muestra por pantalla a que clase pertenece dicha prueba
    """
    print("########## TEST DE BAYES ##########")
    for file in os.listdir(directorio):
        df = pd.read_csv(directorio + '/' + file, header=None)
        pruebaX = np.array(df.iloc[:, :-1])
        pruebaY = np.array(df.iloc[:, -1])
        posMin = pertenenciaBayes(pruebaX, medias)

        print("El archivo {} pertenece a la clase \n{}\n"
             .format(file, vName[posMin]))



##### PRUEBAS #####

X = np.array([
    [3, 5],
    [5, 5],
    [4, 5],
    [3, 1],
    [1, 3],
    [2, 2],
    [1, 1],
    [2, 3],
    [0, 2],
])

Y = np.array([
    'C1',
    'C1',
    'C1',
    'C2',
    'C2',
    'C2',
    'C3',
    'C3',
    'C3',
])

vName = ['C1', 'C2', 'C3']

##### PRUEBAS #####

medias = bayes(X, Y, vName)
testBayes(medias, vName, 'test_bayes')

