#!/usr/bin/env python3
import numpy as np

def calculErreur(matriceInitiale,matriceDecompressee):
    erreur=0
    norm=0
    #Pour chaque canal, on calcule l'erreur
    for k in range (3):
        erreur+=np.linalg.norm(matriceInitiale[:,:,k]-matriceDecompressee[:,:,k])
        norm+=np.linalg.norm(matriceInitiale[:,:,k])
    #Il faut faire attention a prendre la moyenne des 3 normes
    norm/=3
    #Ainsi que la moyenne des 3 erreurs
    erreur=erreur/3
    #On met l'erreur sous forme de pourcentage normalisé
    erreur=erreur/norm*100
    return erreur    