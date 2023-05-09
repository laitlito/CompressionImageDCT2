#!/usr/bin/env python3

def filtreHauteFrequences(mat, seuil):
    for i in range(8):
        for j in range(8):
            if i + j >= seuil:
                mat[i, j] = 0
    return mat