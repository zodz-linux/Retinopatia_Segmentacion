#/usr/bin/python
# -*- coding: utf-8 -*-

import os
from funciones.transformadaMorlet import *
import matplotlib.pyplot as plt
from funciones.groundtruth import *
from funciones.segmentacion import *
from funciones.preprocesamiento import *

########## Varibles Globales
outPath      =(os.getcwd()+"/OutputImages/")
outPathLesion=(os.getcwd()+"/OutputImages/Lesions/")
imagesPath   =(os.getcwd()+"/imagenes/")
############################

def SegmentarVasos(imagen,threshold=140):
    print "\n\t\t*Funcion: Segmentar Vasos ..."
    img= cv2.imread(imagesPath+imagen) # Cargar Imagen
    img=img[:,:,1] # Tomar la Capa Verde
    threshold=120
    out = ApplyMask(img)

    """
    Parametros de la funcion Morlet
    """
    scale = 6.0
    epsilon = 4.0
    k0y = 3.0
    cvgpi = CVGaborProcessedImage(scale, epsilon, k0y)
    """"""

    print " \tPreprocesando        "+imagen
    wavelet = cvgpi.generate(out)

    mask = cv2.imread('mask1.png') #cargar mascara
    mask = mask[:, :, 1]    # Load mask
    wavelet = cv2.bitwise_and(wavelet.real, wavelet.real, mask = mask) # Maskingaxxxxxxx


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

def MomentosGeometricos(imagen,file_xml,size=60):
    print "\t\t*Funcion: Momentos Geometricos ..."
    img= cv2.imread(outPath+imagen) # Cargar Imagen
    img=img[:,:,1] # Tomar la Capa Verde
    GroundTruth=XML2Table(file_xml)
    counter=0
    size=size/2
    attributes=[]
    for lesion in GroundTruth:
        centerX,centerY=lesion[4][0],lesion[4][1] #tomamos como centro el punto representativo
        subimage=img[(centerX-size):(centerX+size),(centerY-size):(centerY+size)]
        temporal=[[centerX,centerY]]
        if subimage.shape == (0, 40) : continue
        if subimage.shape == (40, 0) : continue
        aux=cv2.HuMoments(cv2.moments(subimage))
        temporal.append(aux)
        cv2.imwrite(outPathLesion+file_xml[-25:-4]+"_Lesion_"+str(counter)+".png",subimage)
        counter+=1
        attributes.append(temporal)
    print "Numero de  lesiones: ",counter
    return  attributes


def main():
    print "\n\t\t\tIniciando programa ... \n"

    Images  =[xfile for xfile in  os.listdir(imagesPath) if ".png" in xfile]
    GroundT =[xfile for xfile in  os.listdir(imagesPath)if ".xml" in xfile]
    Images.sort()
    GroundT.sort()
    momentos=[]
    for index in xrange(len(GroundT)):
        CurrentImage=Images[index] # Cargar Imagen
        CurrentXml  =imagesPath+GroundT[index]
        print "\tImagen\t\t\t   Ground Truth"
        print ("\t"+Images[index]+"\t"+GroundT[index])
        SegmentarVasos(CurrentImage)

    pass


if __name__ == "__main__":
    main()
