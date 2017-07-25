#/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cv2
from Functions.transformadaMorlet import *
from Functions.groundtruth import *
from Functions.segmentacion import *
from Functions.preprocesador import *

########## General Paths
imagesPath            =(os.getcwd()+"/Images/")
mask1                 =(os.getcwd()+"/Images/mask1.png")
HistoricalImages      =(os.getcwd()+"/Historical Images/")
######### Segementation Phase
MorletImages          =(os.getcwd()+"/MorletImages/")
SegmentedVesselImages =(os.getcwd()+"/SegmentedBloodVessels/")
EliminatedVessels     =(os.getcwd()+"/EliminatedVessels/")
ThresholdedImages     =(os.getcwd()+"/Thresholding/")
############################


def SegmentarVasos(image):
    Iwavelet= cv2.imread(MorletImages+image,0) # Cargar Imagen
    img_label = image[:18] # nombre del archivo
    Citerio_puntos=5

    print "   -Inicializando ...."
    """ Inicializacion de primera iteracion """
    threshold             = Iwavelet.max() #inicializa el valor del umbral
    Ivessel_past          = Thresholding(Iwavelet,threshold)
    skel                  = Skeletonize(Ivessel_past)
    binarized             = Binarization(skel,1)
    ExtremizedPoints      = ExtremePoints(binarized)
    Iedge_past            = RemoveShortSegments(ExtremizedPoints,41)

    threshold      = threshold-1
    """ Inicializacion de primera iteracion """

    f=open("resultados.txt","a")
    while threshold > 90:


        #Umbralizando imagen
        print "   -Umbralizando         "+img_label,"   Umbral: ",threshold
        #thresholded = Thresholding(Iwavelet,threshold)
        Ivessel = Thresholding(Iwavelet,threshold)
        tmp=Ivessel.copy()#Aqui solo estoy haciendo una copia
        visible=Binary2Maximize(tmp) #Esta funcion solo hace mas visibles
        cv2.imwrite(HistoricalImages+img_label+"_04_Umbralizada.png", visible)

        # Adelgazando imagen
        print "   -Esqueletizando       "+img_label, "   Umbral: ",threshold
        skel=Skeletonize(Ivessel)
        tmp=skel.copy()#Aqui solo estoy haciendo una copia
        visible=Binary2Maximize(tmp)#Esta funcion solo hace mas visibles
        cv2.imwrite(HistoricalImages+img_label+"_05_Esqueletonizada.png", visible)

        print "   -Binarizacion         "+img_label,"   Umbral: ",threshold
        binarized = Binarization(skel,1) #El segundo argumento es el  umbral

        print "   -Puntos Extremos      "+img_label,"   Umbral: ",threshold
        ExtremizedPoints=ExtremePoints(binarized)
        tmp=ExtremizedPoints.copy()
        visible=Binary2Maximize(tmp)
        cv2.imwrite(HistoricalImages+img_label+"_06_PuntosExtremos.png", visible)


        print "   -Segmentos Cortos     "+img_label,"   Umbral: ",threshold
        Iedge=RemoveShortSegments(ExtremizedPoints,41)
        tmp=Iedge.copy()
        visible=Binary2Maximize(tmp)
        cv2.imwrite(HistoricalImages+img_label+"_07_SegmentosCortos.png", visible)

        """Actualizacion de la segmentacion """
        new_points=VaildateByNeighbors(Iedge_past,Iedge,10)#el tercer argumento son el mínimo de puntos nuevos
        print "    -puntos agregados:",len(new_points)
        for point in new_points:
            Ivessel[point[0],point[1]]=1
        aux = Ivessel - Ivessel_past

        print ("\x1b[1A"+"\x1b[2K")*6,#,#solo elimina una linea del std out

        """ Criterio de paro """
        contador=0
        H,W=Ivessel.shape
        for i in xrange(H):
            for j in xrange(W):
                if aux[i,j] > 0:
                    contador +=1
        if contador <= Citerio_puntos:
            break
        #print "pixeles diferentes",contador

        f.write(str(threshold))
        f.write(",  "+str(contador))
        f.write("\n")
        """ Criterio de paro """


        threshold = threshold -1

        visible=Binary2Maximize(Ivessel)
        cv2.imwrite(ThresholdedImages+img_label+"_"+str(256-threshold)+"_.png", visible)

        Iedge_past   = Iedge.copy()
        Ivessel_past = Ivessel.copy()
        """Actualizacion de la segmentacion """


        #res = cv2.bitwise_and(Ivessel, Ivessel, mask = RSS)
    f.close()


    return Ivessel

def main():
    print "\n\t\t\tIniciando programa ... \n"


    #_Variables globales
    mask= cv2.imread(mask1,0)
    Images  =[xfile for xfile in  os.listdir(imagesPath) if "png" in xfile if "diaretdb" in xfile ]
    Images.sort()

    """Preprocesamiento aplicado a  cada imagen """
    for image in (Images):
        aux=image[:-4]+"_filtered.png"
        if not (aux in os.listdir(MorletImages)):
            print "\n  Imagen Actual:\t",image,"\n"
            CurrentFile=cv2.imread(imagesPath+image)
            cv2.imwrite(HistoricalImages+imagen[:-4]+"_01_Original.png", CurrentFile)
            CurrentFile=CurrentFile[:,:,1] #tomando la capa roja
            cv2.imwrite(HistoricalImages+imagen[:-4]+"_02_CapaVerde.png", CurrentFile)
            preprocessed =Preprocessar_imagen(CurrentFile,mask)
            cv2.imwrite(HistoricalImages+image[:-4]+"_03_Morlet.png", preprocessed)
            cv2.imwrite(MorletImages+image[:-4]+"_filtered.png",preprocessed)
    print "  *Imagenes Preprocesadas\n"

    """Segmentacion aplicada a  cada imagen """
    for image in (Images):
        CurrentFile=image[:-4]+"_filtered.png"

        if not (CurrentFile in os.listdir(SegmentedVesselImages)):
            #cv2.imwrite(SegmentedVesselImages+image[:-4]+"_08_Segmented.png", segmented)
            print "\n  *Iniciando Segmentacion\t",CurrentFile
            segmented=SegmentarVasos(CurrentFile)
            #cv2.imwrite(HistoricalImages+image[:-4]+"_08_Segmented.png", segmented)
            cv2.imwrite(SegmentedVesselImages+image[:-4]+"_08_Segmented.png", segmented)


    return


if __name__ == "__main__":
    main()


#imagen=cv2.imread(imagesPath+"diaretdb1_image001.png")
