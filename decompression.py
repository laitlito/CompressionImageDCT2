#!/usr/bin/env python3
import numpy as np

def decompression(matriceCompressee,matriceQuantification,matricePassage):
    matriceDecompressee=np.zeros((8,8))
    matriceIntermediare=np.zeros((8,8))
    
    matriceCompressee=matriceCompressee*matriceQuantification
    
    #DCT inverse : matricePassage^T * matriceCompresse * matricePassage
    matriceIntermediare=np.matmul(matriceCompressee,matricePassage)
    matriceDecompressee=np.matmul(np.transpose(matricePassage),matriceIntermediare)
    
    return matriceDecompressee
