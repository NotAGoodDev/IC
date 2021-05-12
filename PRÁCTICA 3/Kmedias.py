#!/usr/bin/env python
# coding: utf-8

# # K-MEDIAS-BORROSO


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os







def formula(d, b):
    return np.power(
        1 / d,
        (1 / (b - 1))
    )



def dist(x, v):
    return np.sum(
        np.square(x - v)
    )



def calcularDivisor(Xj, V, b = 2):
    divisor = 0
    for k in V:
        res = formula(
            dist(Xj, k),
            b
        )
        divisor += res
        
    return divisor



def calcularP(X, V, b = 2):
    P = np.zeros((V.shape[0], X.shape[0]))
    for j in range(X.shape[0]):
        for i in range(V.shape[0]):
            dividendo = formula(dist(V[i], X[j]), b)
            divisor = calcularDivisor(X[j], V)

            P[i, j] = dividendo / divisor
            
    return P



def recalcularCentros(X, U):
    print()
    fin = []
    for i in range(U.shape[0]):
        aux = []
        for j in range(U.shape[1]):
            aux.append(np.square(U[i, j]) * X[j])

        dividendo = np.sum(np.array(aux), axis=0)
        divisor = np.sum(np.square(U[i, :]))
        fin.append(dividendo / divisor)
        
    return np.array(fin)



def cumpleEpsilon(vAntiguo, vNuevo, epsilon):
    return np.sqrt(np.sum(np.square(vNuevo-vAntiguo))) < epsilon
        
def seguirActualizando(vAntiguo, vNuevo, epsilon):
    actualizar = False
    for i in range(vAntiguo.shape[0]):
        if(not cumpleEpsilon(vAntiguo, vNuevo, epsilon)):
            actualizar = True
            break
            
    return actualizar



def dibujarGrafica(X, V):
    """
    Solo se dibuja la gráfica cuando las V tiene dos dimensiones
    """
    if(V.shape[1] == 2):
        colores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        ax = plt.gca()    

        for i in range(V.shape[0]):

            ax.add_patch(plt.Circle((V[i, 0], V[i, 1]), 2, color=colores[i], alpha=0.4))
            ax.plot(V[i, 0], V[i, 1], 'o', c = 'r')

        ax.plot(X[:, 0], X[:, 1], 'o', c = 'b')

        plt.show()



def trainKMedias(X, V, b, epsilon):
    i = 0
    while True:
        P = calcularP(X, V, b)
        vNuevo = recalcularCentros(X, P)
        if seguirActualizando(V, vNuevo, epsilon):
            print("En la iteración {} los centroides son:\n{}"
                 .format(i, V))
            dibujarGrafica(X, V)
            V = vNuevo
        else:
            print("Hemos terminado en la iteración {}, con los centroides:\n{}\n"
                 .format(i, V))
            dibujarGrafica(X, V)

            break

        i += 1

    return V


def testKMedias(V, vName):
    for file in os.listdir('test'):
        df = pd.read_csv('test/' + file, header=None)
        pruebaX = np.array(df.iloc[:, :-1])
        pruebaY = np.array(df.iloc[:, -1])
        P = calcularP(pruebaX, V)
        posMax = P.argmax()

        print("El archivo {} pertenece al centroide situado en\n{} -> {}\n"
             .format(file, V[posMax], vName[posMax]))

