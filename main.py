#!/usr/bin/env python3
import matplotlib.pyplot as plt
import math as maths
from PIL import Image

#import des fonctions définies dans le dossier
from compression import *
from decompression import *
from filtreHauteFrequences import *
from decompositionMatrice import *
from recompositionImage import *
from calculErreur import *


#Définition de la matrice de passage
matricePassage  =  np.zeros((8, 8))
for i in range(8):
    for j in range(8):
        matricePassage[i, j]  =  (1/2) * maths.cos((2*j+1)*i*maths.pi/16)
matricePassage[0, :] *=  1/maths.sqrt(2)


#Définition de la matrice de quantification
""" matriceQuantification  =  np.array([[16,11,10,16,24,40,51,61],
                                [12,12,13,19,26,58,60,55],
                                [14,13,16,24,40,57,69,56],
                                [14,17,22,29,51,87,80,62],
                                [18,22,37,56,68,109,103,77],
                                [24,35,55,64,81,104,113,92],
                                [49,64,78,87,103,121,120,101],
                                [72,92,95,98,112,100,103,99]])
 """
matriceQuantification = np.array([
    [8, 16, 19, 22, 26, 27, 29, 34],
    [16, 16, 22, 24, 27, 29, 34, 37],
    [19, 22, 26, 27, 29, 34, 34, 38],
    [22, 22, 26, 27, 29, 34, 37, 40],
    [22, 26, 27, 29, 32, 35, 40, 48],
    [26, 27, 29, 32, 35, 40, 48, 58],
    [26, 27, 29, 34, 38, 46, 56, 69],
    [27, 29, 35, 38, 46, 56, 69, 83]
])

#Autre matrice de quantification trouvée sur internet : https://membres-ljk.imag.fr/Valerie.Perrier/SiteWeb/node10.html
#Qui donne des resultats assez similaires 
""" matriceQuantification = np.array([[4, 7, 10, 13, 16, 19, 22, 25],
                                        [7, 10, 13, 16, 19, 22, 25, 28],
                                        [10, 13, 16, 19, 22, 25, 28, 31],
                                        [13, 16, 19, 22, 25, 28, 31, 34],
                                        [16, 19, 22, 25, 28, 31, 34, 37],
                                        [19, 22, 25, 28, 31, 34, 37, 40],
                                        [22, 25, 28, 31, 34, 37, 40, 43],
                                        [25, 28, 31, 34, 37, 40, 43, 46]]) """

#On peut également faire avec la matrice Hilbert inverse qui donne 83% de compression pour 10% d'erreur
""" def hilbertInverse(n):
    H = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            H[i, j] = 1 * (i + j + 1)
    return H.astype(int)
matriceQuantification = hilbertInverse(8) """



def mainPNG():
    # On charge l'image. Le dossier photos en contient d'autres, il est possible de changer
    image  =  plt.imread("photos/linux.png")

    # On transforme en tableau d'entiers de 8 bits
    image  =  (image * 255).astype(int)
    # On centre l'image autour de 0 (entre -127 et 128)
    image -=  128

    # On récupère le nombre de lignes, de colonnes et de canaux
    nbLignes, nbColonnes, nbCanal  =  np.shape(image)

    # On tronque l'image à des multiples de 8 (le plus grand (multiple de 8) contenu dans la hauteur puis dans la largeur)
    nbLignes = int(nbLignes/8)*8
    nbColonnes = int(nbColonnes/8)*8
    
    matriceInitiale = image[0:nbLignes,0:nbColonnes,0:3]

    #On décompose l'image pour chaque canal de couleur : rouge, vert et bleu
    canalRouge = decompositionMatrice(matriceInitiale[:,:,0],nbLignes,nbColonnes)
    canalVert = decompositionMatrice(matriceInitiale[:,:,1],nbLignes,nbColonnes)
    canalBleu = decompositionMatrice(matriceInitiale[:,:,2],nbLignes,nbColonnes)

    #Le nombre de coeffs non nuls sert à calculer le taux de compression
    nbCoefNonNul = 0
    for i in range(len(canalVert)):
        #On applique le filtre haute fréquences sur les images compressées
        #Pour le filtreHauteFrequence, tester avec 6, 4 ou 2
        #6 : 89% compression et 11% erreur
        #4 : 92% compression et 17% erreur
        #2 : 96% compression et 29% erreur
        #On peut également choisir des valeurs différentes pour chaque canal
        #Pour image lourde, si haut nombre pour haute fréquence donc mettre 1
        canalRouge[i] = filtreHauteFrequences(compression(canalRouge[i],matriceQuantification,matricePassage),2)
        canalVert[i] = filtreHauteFrequences(compression(canalVert[i],matriceQuantification,matricePassage),2)
        canalBleu[i] = filtreHauteFrequences(compression(canalBleu[i],matriceQuantification,matricePassage),2)
        nbCoefNonNul+= np.count_nonzero(canalRouge[i])+np.count_nonzero(canalVert[i])+np.count_nonzero(canalBleu[i])

    #Calcul du taux de compression    
    tauxDeCompression = (1-nbCoefNonNul/(nbLignes*nbColonnes*3))*100

    for i in range (len(canalRouge)):
        #On décompresse après avoir appliqué le filtre haute fréquences
        canalRouge[i] = decompression(canalRouge[i],matriceQuantification,matricePassage)
        canalVert[i] = decompression(canalVert[i],matriceQuantification,matricePassage)
        canalBleu[i] = decompression(canalBleu[i],matriceQuantification,matricePassage)
    #On recompose l'image
    canalRouge = recompositionImage(canalRouge,nbLignes,nbColonnes)
    canalVert = recompositionImage(canalVert,nbLignes,nbColonnes)
    canalBleu = recompositionImage(canalBleu,nbLignes,nbColonnes)
    
    matriceDecompressee = np.zeros((nbLignes,nbColonnes,3))
    
    matriceDecompressee[:,:,0] = canalRouge
    matriceDecompressee[:,:,1] = canalVert
    matriceDecompressee[:,:,2] = canalBleu

    erreur = calculErreur(matriceInitiale,matriceDecompressee)

    #Affichage dans le terminal du taux de compression et de l'erreur
    print("Taux de compression : ",tauxDeCompression, "%")
    print("Erreur : ",erreur, "%")
    #On repasse sur des entiers entre 0 et 255
    matriceDecompressee+= 128

    #On s'assure que les valeurs sont comprises entre 0 et 255, sinon, elles sont tronquées à 0 ou 255
    for k in range (np.shape(matriceDecompressee)[2]):
        for i in range (np.shape(matriceDecompressee)[0]):
            for j in range (np.shape(matriceDecompressee)[1]):
                if matriceDecompressee[i][j,k] < 0:
                    matriceDecompressee[i][j,k] = 0
                if matriceDecompressee[i][j,k] > 255:
                    matriceDecompressee[i][j,k] = 255
    
    #On passe sur des réels entre 0 et 1
    matriceDecompressee = matriceDecompressee/255

    plt.imsave("ImagesCompressées/Image compressée.png",matriceDecompressee)
    imageCompressee = Image.open("ImagesCompressées/Image compressée.png")
    imageCompressee.show()


def mainJPG():
    # On charge l'image. Le dossier photos en contient d'autres, il est possible de changer
    image  =  plt.imread("photos/lion.jpg")
    image_array = np.array(image)
    image_array = image_array.dot(np.array([[0.299, 0.587, 0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]]))
    image_array -= 128


    nbLignes, nbColonnes, nbCanal  =  np.shape(image)

    # On tronque l'image à des multiples de 8 (le plus grand (multiple de 8) contenu dans la hauteur puis dans la largeur)
    nbLignes = int(nbLignes/8)*8
    nbColonnes = int(nbColonnes/8)*8
    
    matriceInitiale = image[0:nbLignes,0:nbColonnes,0:3]

    #On décompose l'image pour chaque canal de couleur : rouge, vert et bleu
    Y_channel = decompositionMatrice(matriceInitiale[:,:,0],nbLignes,nbColonnes)
    U_channel = decompositionMatrice(matriceInitiale[:,:,1],nbLignes,nbColonnes)
    V_channel = decompositionMatrice(matriceInitiale[:,:,2],nbLignes,nbColonnes)

    #Le nombre de coeffs non nuls sert à calculer le taux de compression
    nbCoefNonNul = 0
    for i in range(len(U_channel)):
        #On applique le filtre haute fréquences sur les images compressées
        #Pour le filtreHauteFrequence, tester avec 6, 4 ou 2
        #6 : 89% compression et 11% erreur
        #4 : 92% compression et 17% erreur
        #2 : 96% compression et 29% erreur
        #On peut également choisir des valeurs différentes pour chaque canal
        #Pour image lourde, si haut nombre pour haute fréquence donc mettre 1
        Y_channel[i] = filtreHauteFrequences(compression(Y_channel[i],matriceQuantification,matricePassage),2)
        U_channel[i] = filtreHauteFrequences(compression(U_channel[i],matriceQuantification,matricePassage),2)
        V_channel[i] = filtreHauteFrequences(compression(V_channel[i],matriceQuantification,matricePassage),2)
        nbCoefNonNul+= np.count_nonzero(Y_channel[i])+np.count_nonzero(U_channel[i])+np.count_nonzero(V_channel[i])

    #Calcul du taux de compression    
    tauxDeCompression = (1-nbCoefNonNul/(nbLignes*nbColonnes*3))*100

    for i in range (len(Y_channel)):
        #On décompresse après avoir appliqué le filtre haute fréquences
        Y_channel[i] = decompression(Y_channel[i],matriceQuantification,matricePassage)
        U_channel[i] = decompression(U_channel[i],matriceQuantification,matricePassage)
        V_channel[i] = decompression(V_channel[i],matriceQuantification,matricePassage)
    #On recompose l'image
    Y_channel = recompositionImage(Y_channel,nbLignes,nbColonnes)
    U_channel = recompositionImage(U_channel,nbLignes,nbColonnes)
    V_channel = recompositionImage(V_channel,nbLignes,nbColonnes)
    
    matriceDecompressee = np.zeros((nbLignes,nbColonnes,3))
    
    matriceDecompressee[:,:,0] = Y_channel
    matriceDecompressee[:,:,1] = U_channel
    matriceDecompressee[:,:,2] = V_channel

    erreur = calculErreur(matriceInitiale,matriceDecompressee)

    #Affichage dans le terminal du taux de compression et de l'erreur
    print("Taux de compression : ",tauxDeCompression, "%")
    print("Erreur : ",erreur, "%")
    #On repasse sur des entiers entre 0 et 255
    matriceDecompressee+= 128

    #On s'assure que les valeurs sont comprises entre 0 et 255, sinon, elles sont tronquées à 0 ou 255
    for k in range (np.shape(matriceDecompressee)[2]):
        for i in range (np.shape(matriceDecompressee)[0]):
            for j in range (np.shape(matriceDecompressee)[1]):
                if matriceDecompressee[i][j,k] < 0:
                    matriceDecompressee[i][j,k] = 0
                if matriceDecompressee[i][j,k] > 255:
                    matriceDecompressee[i][j,k] = 255
    
    #On passe sur des réels entre 0 et 1
    matriceDecompressee = matriceDecompressee/255

    plt.imsave("ImagesCompressées/Image compressée.jpg",matriceDecompressee)
    imageCompressee = Image.open("ImagesCompressées/Image compressée.jpg")
    imageCompressee.show()



#À utiliser pour une image PNG
mainPNG()

#À utiliser pour une image JPG (marche mal)
#mainJPG()