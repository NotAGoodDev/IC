#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from anytree import Node, RenderTree



headers = pd.read_csv('AtributosJuego.txt', header=None)
game = pd.read_csv('Juego.txt', sep=',', header=None)




## 'Hard to understand' because a lot of code, but efficient
## because the costs ~ O(n * m) but only once

def countValues_PosNeg(listaDeAtributos, listaDeEjemplos):
    """
        Returns dictionaries c, pn
        
        c: Counts the times that attributes repeats
        pn: Counts the number of positives and negatives of attributes
    """
    
    c = dict()                                      # Counter of total
    pn = dict()                                     # Counter of pos/neg

    for i in range(listaDeEjemplos.shape[1] - 1):   # Inverted axis
        tipo = listaDeAtributos[i][0]               # c[A], c[B]...
        lastValue = listaDeEjemplos.shape[1] - 1    # Last column
        
        for j in range(listaDeEjemplos.shape[0]):   # Inverted axis
            value = listaDeEjemplos[i][j]           # Table's value
            result = listaDeEjemplos[lastValue][j]  # Positive or Negative
            
            
            if tipo in c:                           # Column's name
                if value in c[tipo]:                # Table's value exists
                    c[tipo][value] += 1             # Add 1 to counter
                else :
                    c[tipo][value] = 1              # Init value
                    
            else :
                c[tipo] = dict()
                c[tipo][value] = 1                  # Init value
                
                
                
            if tipo in pn:                          # Column's name
                if value in pn[tipo]:               # Table's value exists
                    if result in pn[tipo][value] :  # pn[A][a1][+] exists?
                        pn[tipo][value][result] += 1
                    else :
                        pn[tipo][value][result] = 1
                        
                else :                              # Init value
                    pn[tipo][value] = dict()
                    pn[tipo][value][result] = 1
                    
            else:                                   # Init value
                    pn[tipo] = dict()               
                    pn[tipo][value] = dict()
                    pn[tipo][value][result] = 1
                
            
    return (c, pn)           




def getPN(dic):
    """
    Returns the positive and negatives values of dictionarie
    -> Doesnt iterate over dictionaries so it should be key : value
    """
    pos = 0
    neg = 0
    
    for v in dic.keys():
        if (
            v == "Si" or v == "si"
            or v == "S" or v == "s"
            or v == "Positivo" or v == "positivo"
            or v == "Positive" or v == "positive"
            or v == "Verdadero" or v == "verdadero"
            or v == "True" or v == "true"
            or v == "+"
        ):
            pos = dic[v]
        else :
            neg = dic[v]
            
    return (pos, neg)




def merito(p, n):
    """
    Calculates a part of the merit from positive and negative values (integers)
    Returns the merit
    """
    term1 = 0
    term2 = 0
    
    if p == 0:
        term1 = 0
    else:
        term1 = -p * np.log2(p)
        
    if n == 0:
        term2 = 0
    else:
        term2 = n * np.log2(n)
        
        
    return term1 - term2 




def meritoTotal(c, pn, total):
    """
    Calculates the merit from dictionaries 'count of values' and 'positive and negatives',
    we need the length of 'listaDeEjemplos' too
    Returns a dictionary with all the merit
        E.g: merito['A'] = 0.37
    """
    m = dict()   # Diccionario de merito
    
    for tipo in c.keys():
        m[tipo] = 0

        for value in c[tipo].keys():
            p, n = getPN(pn[tipo][value])
            a = p + n
            infor = merito(p/a, n/a)
            m[tipo] += ((a/total) * infor)
        
    return m
            




def removeValues(lista, value, position):
    """
    This function removes the values that are innecesary (column and rows
    that doesnt have the value)
    
    Returns the list
    """
    aux = []
    lista = lista.T
    
    for i in range(lista.shape[1]):
        
        if(value == lista[i][position]):
            temp = []
            
            for x in range(lista.shape[0]):
                if(x != position):
                    temp.append(lista[i][x])   
            
            aux.append(temp)
            
            
    return aux




def divideNodes(listaDeAtributos, listaDeEjemplos, minimo):
    """
    This function divides the main list into small pieces without
    the wished column and the examples that doesnt have the value, 
    for example:
        a1,b3,c2,+
        a2,b1,c1,+
        a1,b2,c1,-
        a1,b1,c3,+
        a2,b3,c3,-
        a1,b1,c1,-
        a1,b2,c1,-
        a2,b3,c2,+


        -> c1        
            a2,b1,+
            a1,b2,-
            a1,b1,-
            a1,b2,-
            
        -> c2
            a1,b3,+
            a2,b3,+
            
        -> c3
            a1,b1,+
            a2,b3,-
    
    Returns the divided lists and the values removed.
    """
    
    pos = 0
    
    for i in range(listaDeAtributos.shape[1] - 1):
        if listaDeAtributos[i][0] == minimo:
            pos = i
        
    r = []
    
    visited = dict()
    values = []
    
    for v in listaDeEjemplos[pos]:
        if v not in visited:  # Didnt visited -> To dont repeat values
            visited[v] = True
            x = removeValues(listaDeEjemplos, v, pos)
            r.append(x)
            values.append(v)
            
    return r, np.array(values)




def onlyOneResult(c, pn):
    """
    This function returns the total count (integer) of positive and negative
    values
    """
    p = 0
    n = 0
    tipo = next(iter(pn.items()))[0]           # First element of dictionarie

    for value in c[tipo].keys():
        pAux, nAux = getPN(pn[tipo][value])
        p += pAux
        n += nAux
        
    return p, n



def deleteAtribute(listaDeAtributos, column):
    """
    Deletes one column of DataFrame 'listaDeAtributos' from a name
    
    If you want to delete listaDeAtributos['Columna2'],
    you should pass (listaDeAtributos, 'Columna2')
    
    Returns a DataFrame with the column deleted.
    """
    
    posToDelete = np.where(listaDeAtributos == column)                       # Get pos of min
    listaDeAtributos = np.delete(np.array(listaDeAtributos), posToDelete)    # Array and delete
    return pd.DataFrame(listaDeAtributos).T                                  # Again pandas and T



def formatLine(v):
    """
    Deletes ' [ ] ,
    from a vector and returns a string
    Print function
    """
    return str(v).replace('\'', '').replace('[', '').replace(']','').replace(',','')


def printTree(tree):
    """
    Prints a tree from anytree library
    """
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name.upper()))

        for line in node.lines:
            formattedSon = formatLine(line)
            print("%s%s" % (fill , formattedSon))
        print("%s%s" % (fill, " "))
    
    print('-' * 30, '\n\n')




def id3(listaDeAtributos, listaDeEjemplos, superiorDecisionTree, superiorExplainableTree):
    """
    Manages the id3 algorithm
        listaDeAtributos: Pandas Dataframe
        listaDeEjemplos: Pandas Dataframe
        superiorDecisionTree: Anytree Node
        superiorExplainableTree: Anytree Node
        
    Doesnt return anything because we need to manage Anytree nodes -> Pointers
    
    """
    
    c, pn = countValues_PosNeg(listaDeAtributos, listaDeEjemplos)     # Dictionaries
    p, n = onlyOneResult(c, pn)                                       # Any - or + ?
    
    if(n != 0 and p != 0):
        total = listaDeEjemplos.shape[0]                              # Count
        m = meritoTotal(c, pn, total)                                 # Get the merit
        minimo, meritoMin = min(m.items(), key=lambda x: x[1])        # Get the minimum
        meritoMin = np.round(meritoMin, 3)
        r, values = divideNodes(listaDeAtributos,                     # Divide tree in branches
                        listaDeEjemplos,
                        minimo
                       )
        
        # Manage the 'listaDeAtributos' dataframe
        deleteAtribute(listaDeAtributos, minimo[0][0])

        
        # Manage the recusivity
        i = 0                                                         # For list of values
        for sub in r:
            newExamples = pd.DataFrame(sub)
            nodeDecisionTree = Node(minimo,
                                    superiorDecisionTree,
                                    lines = [values[i]]
                                   )
            
            nodeExplainableTree = Node(values[i] + "\t\tMerito: " + str(meritoMin),
                                       superiorExplainableTree,
                                       lines = sub
                                      )
            
            id3(listaDeAtributos, newExamples, nodeDecisionTree, nodeExplainableTree)
            
            i += 1
            
    # Manage the leaf of the tree
    else:
        lastValue = len(listaDeEjemplos.T) - 1
        value = listaDeEjemplos[lastValue][0]
        node = Node(value, superiorDecisionTree, lines = [])



decisionTree = Node("Decision Tree", lines = [])
explainableTree = Node("Solution Explained", lines = [])
id3(headers, game, decisionTree, explainableTree)
printTree(decisionTree)
printTree(explainableTree)

