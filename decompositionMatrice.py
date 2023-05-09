#!/usr/bin/env python3

def decompositionMatrice(mat, numeroLigne, numeroColonne):
    #Décomposition de la matrice (image) en plusieurs blocs 8x8
    sousMatrices = []
    for x in range(0, numeroLigne, 8):
        for y in range(0, numeroColonne, 8):
            sousMatrices.append(mat[x:x+8, y:y+8])
    return sousMatrices
