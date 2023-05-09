#!/usr/bin/env python3
import numpy as np

def compression(mat, matriceQuantification, matricePassage):
    matriceTransformee = np.zeros((8, 8))
    matriceIntermediaire = np.zeros((8, 8))
    
    #DCT 2 par changement de base : matriceTransformee = matricePassage * mat * matricePassage^T
    matriceIntermediaire = np.matmul(mat, np.transpose(matricePassage))
    matriceTransformee = np.matmul(matricePassage, matriceIntermediaire)
    
    # On divise par la matrice de quantification
    matriceTransformee = np.divide(matriceTransformee, matriceQuantification)
    matriceTransformee = matriceTransformee.astype(int)
    
    return matriceTransformee