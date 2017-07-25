import cv2
import numpy as np
from transformadaMorlet import *
import os


def ApplyMaskNegative(image, mask):
    img2 = image.copy()
    img2 = 255 - img2
    img = cv2.bitwise_and(img2, img2, mask = mask)
    return img

def ApplyMaskPositive(image, mask):
    img2 = image.copy()
    img = cv2.bitwise_and(img2, img2, mask = mask)
    return img


def extend_image(img,window_size=12,umbral=19,iterations=25):
    # variables creation
    print "  *Extendiendo Bordes\n"
    H,W=img.shape
    reading_image=np.zeros((H+(window_size*4),W+(window_size*4)),dtype=np.int)
    reading_image[(window_size*2):(window_size*2)+H,(window_size*2):(window_size*2)+W]=img
    writing_image=reading_image.copy()
    H,W=reading_image.shape
    neighbors=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    neighbors=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    # variables creation

    # starting mark edge
    for it in xrange(iterations):
        print "\x1b[1A"+"\x1b[2K","\t --> ",((it+1)/float(iterations))*100," %"
        for  i in xrange(H):
            for j in xrange(W):
                if reading_image[i,j] > umbral:
                    for p in [[1,0],[0,1],[-1,0],[0,-1]]:
                        if  p[0]+i >= 0 and p[0]+i < H and p[1]+j >=0 and p[1]+j < W:
                            if reading_image[p[0]+i,p[1]+j] < umbral:
                                writing_image[p[0]+i,p[1]+j]=-1
        reading_image=writing_image.copy()
        # marked  edge
        for  i in xrange(H):
            for j in xrange(W):
                if reading_image[i,j]== -1:
                    not_nulls=0   # count not null values
                    local_value=0 # it will be the mean value
                    for p in  neighbors:
                        if  p[0]+i >= 0 and p[0]+i < H and p[1]+j >=0 and p[1]+j < W:
                            if reading_image[i+p[0],j+p[1]] > umbral:
                                not_nulls+=1
                                local_value+=reading_image[i+p[0],j+p[1]]
                    local_value/=float(not_nulls)
                    reading_image[i,j]=local_value
                    writing_image[i,j]=local_value
        reading_image=writing_image.copy()
    return reading_image

def  AdjustContrast(image):
    (current_height, current_width) = image.shape
    avg = np.mean(image)
    stddev = np.std(image)
    for i in xrange(current_height):
        for j in xrange(current_width):
            image[i][j] = (image[i][j] - avg) / stddev
    minimum = np.min(image)
    maximum = np.max(image)
    for i in xrange(current_height):
        for j in xrange(current_width):
            image[i][j] = (image[i][j] - minimum) / (maximum - minimum)
    return  image


def Preprocessar_imagen(image,mask):
    window_size=12
    umbral=20
    iterations=20
    #parametros wavelet
    scale = 8.0
    epsilon = 4.0
    k0y = 3.0

    #parametros enmascaramiento
    H,W=mask.shape

    # tomado capa inversa
    extended=extend_image(image)


    extended=255-extended
    #extended = extended / 255.0
    cvgpi = CVGaborProcessedImage(scale, epsilon, k0y)
    print "  *Generando Wavelet\n"
    wavelet = cvgpi.generate(extended)
    new=wavelet.real[(window_size*2):(window_size*2)+H,(window_size*2):(window_size*2)+W]

    new=255-new
    out = ApplyMaskNegative(new, mask)
    print "  *Ajustando Contraste\n"
    out = AdjustContrast(out) #la imagen  es normalizada  y estandarizada (0,1)
    out=out*255
    return out
