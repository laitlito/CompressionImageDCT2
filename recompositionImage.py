#!/usr/bin/env python3
import numpy as np

def recompositionImage(canalCouleur,nombreLignes,nombreColonnes):
    #On initialise une matrice vide qui a la taille de la matrice recomposée
    matriceDecompressee=np.zeros((nombreLignes,nombreColonnes))
    
    compteurMatrice=0
    for ligne in range (int(nombreLignes/8)):
        compteurCols=0
        while compteurCols<int(nombreColonnes/8):
            matrice=canalCouleur[compteurMatrice]
            for i in range(8):  
                for j in range(8):
                    matriceDecompressee[ligne*8+i,compteurCols*8+j]=matrice[i,j]
            compteurCols+=1
            compteurMatrice+=1
    return matriceDecompressee