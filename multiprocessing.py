#/usr/bin/python
# -*- coding: utf-8 -*-

import os
from functions.segmentacion import *
from functions.preprocesamiento import *
from functions.paralelismo import *
import cv2

########## Varibles Globales
outPath      =(os.getcwd()+"/OutputImages/")
outPathLesion=(os.getcwd()+"/OutputImages/Lesions/")
imagesPath   =(os.getcwd()+"/Images/")
############################

def SegmentarVasos(imagen):
    print "\n\t\t*Funcion: Segmentar Vasos ..."
    img= cv2.imread(imagesPath+imagen) # Cargar Imagen
    img=img[:,:,1] # Tomar la Capa Verde
    threshold=140

    print " \tUmbralizacion        "+imagen
    thresholded = Thresholding(wavelet.real,threshold)
    cv2.imwrite(outPath+imagen[:-4]+"_1Umbralizada.png", thresholded)

    skel=skeletonize(thresholded)
    print " \tEsqueletizando       "+imagen
    cv2.imwrite(outPath+imagen[:-4]+"_2Esqueletizada.png", skel)


    print " \tBinarizacion         "+imagen
    binarized = Binarization(skel,1)

    print " \tPuntos Extremos      "+imagen
    ExtremizedPoints=ExtremePoints(binarized)
    #Aqui solo estoy haciendo una copia donde se puedan notar los puntos
    tmp=ExtremizedPoints.copy()
    vs=Binary2Maximize(tmp)
    cv2.imwrite(outPath+imagen[:-4]+"_3PuntosExtremos.png", vs)


    print " \tEliminando Segmentos "+imagen
    RSS=RemoveShortSegments(ExtremizedPoints,41)
    #Aqui solo estoy haciendo una copia donde se puedan notar los puntos
    tmp=RSS.copy()
    vs=Binary2Maximize(tmp) #Esta funcion solo hace mas visibles
    cv2.imwrite(outPath+imagen[:-4]+"_4SegmentosCortos.png", vs)

    return

def main():
    print "Iniciando programa ... \n"
    Images  =[xfile for xfile in  os.listdir(imagesPath) if "Filtered.png" in xfile]
    Images.sort()
    Create4Process(Images,SegmentarVasos)
    pass

if __name__ == "__main__":
    main()
