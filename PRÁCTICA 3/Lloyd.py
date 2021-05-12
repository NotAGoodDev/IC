#!/usr/bin/env python
# coding: utf-8

# In[20]:


import numpy as np
import pandas as pd
import os


# In[21]:


# X = np.array([
#     [1, 1],
#     [1, 3],
#     [1, 5],
#     [1, 2],
#     [2, 3],
#     [2, 3],
#     [6, 4],
#     [6, 1],
#     [7, 3],
#     [7, 5],
# ])

# V = np.array([
#     [1.0, 4.0],
#     [7.0, 2.0],
# ])


# In[22]:


def calcularDistancias(x, V):      
    posOpt = None
    distOpt = np.inf

    for j in range(V.shape[0]):
        dist = np.sum(np.square(x - V[j]))
        if (distOpt > dist):
            distOpt = dist
            posOpt = j

    return posOpt


# In[23]:


def distEuclidea(A, B):
    return np.sqrt(np.sum(np.square(A - B)))


# In[24]:


def testLloyd(V, vName):
    print("########## TEST DE LLOYD ##########")
    for file in os.listdir('test'):
        df = pd.read_csv('test/' + file, header=None)
        pruebaX = np.array(df.iloc[:, :-1])
        pruebaY = np.array(df.iloc[:, -1])
        distancias = np.sum(np.square(pruebaX - V), axis=1)
        posMin = np.argmin(np.array(distancias))

        print("El archivo {} pertenece a la clase \n{}\n"
             .format(file, vName[posMin]))
        


# In[45]:


def lloyd(X, V, gamma, kMax, epsilon):
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


# In[ ]:





# In[ ]:




