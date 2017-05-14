#/usr/bin/python
import os
from funciones.groundtruth import *
from funciones.preprocesamiento import *
from funciones.segmentacion import *
from funciones.attributes import *

def main():
    print "\n\t\t\tIniciando programa ... \n"
    images=[xfile for xfile in  os.listdir(os.getcwd()+"/Images") if ".png" in xfile]
    images.sort()
    for xfile in images:
        print "\n\t",xfile,"\n"
        SingleSegmentation(xfile)
        #break
        threshold=175
        img = cv2.imread("Images/"+xfile) # read file
        print " \tPreprocesando        ",xfile
        image= preprocesar(img)
        cv2.imwrite("OutputImages/"+xfile[:-4]+"_1Preprocesada.png",image)

        print " \tUmbralizacion        ",xfile
        thresholded = Thresholding(image,threshold)
        cv2.imwrite("OutputImages/"+xfile[:-4]+"_2Umbralizada.png", thresholded)


        print " \tEsqueletizando       ",xfile
        skel=skeletonize(thresholded)
        cv2.imwrite("OutputImages/"+xfile[:-4]+"_3Esqueletizada.png", skel)

        print " \tBinarizacion         ",xfile
        binary = Binarization(skel,1)


        print " \tPuntos Extremos      ",xfile
        ep=ExtremePoints(binary)
        tmp=ep.copy()
        vs=Binary2Maximize(tmp)
        cv2.imwrite("OutputImages/"+xfile[:-4]+"_4PuntosExtremos.png", vs)

        print " \tEliminando Segmentos ",xfile
        RSS=RemoveShortSegments(ep,41)
        tmp=RSS.copy()
        vs=Binary2Maximize(tmp)
        cv2.imwrite("OutputImages/"+xfile[:-4]+"_5SegmentosCortos.png", vs)
    pass

if __name__ == "__main__":
    main()
