#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import os



def calcularDistancias(x, V):
    """
        Función que calcula la distancia de un punto X[i] respecto a los centroides
        Devuelve la posición (en el array) del centroide más cercano
    """
    posOpt = None
    distOpt = np.inf

    for j in range(V.shape[0]):
        dist = np.sum(np.square(x - V[j]))
        if (distOpt > dist):
            distOpt = dist
            posOpt = j

    return posOpt



def distEuclidea(A, B):
    """
    Calcula la distancia euclidea de un punto A respecto a B
    """
    return np.sqrt(np.sum(np.square(A - B)))



def testLloyd(V, vName, directorio='test'):
    """
    Función que calcula la distancia de todas las pruebas ubicadas en la carpeta test a partir del
    vector de centroides, su etiqueta, y el nombre de la carpeta.
    No devuelve nada, muestra por pantalla a que clase pertenece dicha prueba
    """
    
    print("########## TEST DE LLOYD ##########")
    for file in os.listdir(directorio):
        df = pd.read_csv(directorio + '/' + file, header=None)
        pruebaX = np.array(df.iloc[:, :-1])
        pruebaY = np.array(df.iloc[:, -1])
        distancias = np.sum(np.square(pruebaX - V), axis=1)
        posMin = np.argmin(np.array(distancias))

        print("El archivo {} pertenece a la clase \n{}\n"
             .format(file, vName[posMin]))
        



def lloyd(X, V, gamma, kMax, epsilon):
    """
    Gestiona el algoritmo de Lloyd, devuelve los centroides entrenados a partir de
    un conjunto de datos X, los centroides iniciales, un valor gamma, unas iteraciones
    máximas y un error mínimo epsilon
    """
    print("\n########## ENTRENAMIENTO DE LLOYD ##########\n")

    for it in range(kMax):
        vNuevo = V.copy()
        
        for i in range(X.shape[0]):
            pos = calcularDistancias(X[i], V)
            vNuevo[pos] = vNuevo[pos] + gamma * (X[i] - vNuevo[pos])

        seguir = False
        for i in range(V.shape[0]):
            if(distEuclidea(V[i], vNuevo[i]) >= epsilon):
                seguir = True

        if(seguir):
            print("ITERACIÓN {}.\nAntiguo:\n{}\n\nNuevo\n{}\n"
                 .format(it + 1, V, vNuevo))
            V = vNuevo
            
        else:
            break

            
        print("-"*30)
        
    return V


##### PRUEBAS #####

X = np.array([
    [1, 1],
    [1, 3],
    [1, 5],
    [1, 2],
    [2, 3],
    [2, 3],
    [6, 4],
    [6, 1],
    [7, 3],
    [7, 5],
])

V = np.array([
    [1.0, 4.0],    # C1
    [7.0, 2.0],    # C2
])

vName = ['C1', 'C2']

gamma = .1
kMax = 10
epsilon = .1

##### PRUEBAS #####


vNuevo = lloyd(X, V, gamma, kMax, epsilon)
testLloyd(vNuevo, vName, 'test_lloyd')
