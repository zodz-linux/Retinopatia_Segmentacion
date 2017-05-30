#/usr/bin/python
# -*- coding: utf-8 -*-

import os
from funciones.transformadaMorlet import *
import matplotlib.pyplot as plt
from funciones.groundtruth import *
from funciones.segmentacion import *
from funciones.preprocesamiento import *
from funciones.paralelismo import *

########## Varibles Globales
outPath      =(os.getcwd()+"/OutputImages/")
outPathLesion=(os.getcwd()+"/OutputImages/Lesions/")
imagesPath   =(os.getcwd()+"/imagenes/")
############################

def SegmentarVasos(imagen):
    print "\n\t\t*Funcion: Segmentar Vasos ..."
    img= cv2.imread(imagesPath+imagen) # Cargar Imagen
    img=img[:,:,1] # Tomar la Capa Verde
    threshold=140
    out = ApplyMask(img)

    """
    Parametros de la funcion Morlet
    """
    scale = 4.0
    epsilon = 4.0
    k0y = 3.0
    cvgpi = CVGaborProcessedImage(scale, epsilon, k0y)
    print " \tPreprocesando        "+imagen
    wavelet = cvgpi.generate(out)
    cv2.imwrite(outPath+imagen[:-4]+"_1Preprocesada.png",wavelet.real)

    print " \tUmbralizacion        "+imagen
    thresholded = Thresholding(wavelet.real,threshold)
    cv2.imwrite(outPath+imagen[:-4]+"_2Umbralizada.png", thresholded)

    skel=skeletonize(thresholded)
    print " \tEsqueletizando       "+imagen
    cv2.imwrite(outPath+imagen[:-4]+"_3Esqueletizada.png", skel)


    print " \tBinarizacion         "+imagen
    binarized = Binarization(skel,1)

    print " \tPuntos Extremos      "+imagen
    ExtremizedPoints=ExtremePoints(binarized)
    #Aqui solo estoy haciendo una copia donde se puedan notar los puntos
    tmp=ExtremizedPoints.copy()
    vs=Binary2Maximize(tmp)
    cv2.imwrite(outPath+imagen[:-4]+"_4PuntosExtremos.png", vs)


    print " \tEliminando Segmentos "+imagen
    RSS=RemoveShortSegments(ExtremizedPoints,41)
    #Aqui solo estoy haciendo una copia donde se puedan notar los puntos
    tmp=RSS.copy()
    vs=Binary2Maximize(tmp) #Esta funcion solo hace mas visibles
    cv2.imwrite(outPath+imagen[:-4]+"_5SegmentosCortos.png", vs)

    pass

def main():
    print "Iniciando programa ... \n"
    Images  =[xfile for xfile in  os.listdir(imagesPath) if ".png" in xfile]
    Images.sort()
    Create4Process(Images,SegmentarVasos)
    pass

if __name__ == "__main__":
    main()
