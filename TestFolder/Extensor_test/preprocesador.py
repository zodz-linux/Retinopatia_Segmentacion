import cv2
import numpy as np
from transformadaMorlet import *
import os

def ApplyMask(image, mask):
    #mask = mask[:, :, 1]    # Load mask
    #image = image[:, :, 1]  # Take green layer
    img2 = image.copy()
    img2 = 255 - img2
    img = cv2.bitwise_and(img2, img2, mask = mask) # Maskingaxxxxxxx
    return img

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

def extend_image(file_name,window_size=12,umbral=20,iterations=20):
    # variables creation
    print "\t Funcion: Extender Bordes\n"
    img=cv2.imread(file_name)
    img=img[:,:,1] # green  layer
    H,W=img.shape
    reading_image=np.zeros((H+(window_size*4),W+(window_size*4)),dtype=np.int)
    reading_image[(window_size*2):(window_size*2)+H,(window_size*2):(window_size*2)+W]=img
    writing_image=reading_image.copy()
    H,W=reading_image.shape
    neighbors=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    # variables creation

    # starting mark edge
    for it in xrange(iterations):
        print "\t Iteracion:",it+1,"/",iterations
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

def Preprocessar_imagen(image):
    #parametros wavelet
    scale = 8.0
    epsilon = 4.0
    k0y = 3.0

    #parametros extensor
    window_size=12
    umbral=20
    iterations=20

    #parametros enmascaramiento
    #file_mask='mask.png'
    mask= cv2.imread('mask.png')
    mask=mask[:,:,1]
    H,W=mask.shape


    #starting preprocessing
    print "\n\nIniciando preprocesamiento:\t",image
    extended=extend_image(file_name,window_size,umbral,iterations)

    # tomado capa inversa
    extended=255-extended
    #extended = extended / 255.0
    cvgpi = CVGaborProcessedImage(scale, epsilon, k0y)
    print "\nFuncion: Generando wavelet\n"
    wavelet = cvgpi.generate(extended)
    #print('Min = {}, max = {}'.format(np.min(wavelet.real), np.max(wavelet.real)))
    #now we cut the image
    new=wavelet.real[(window_size*2):(window_size*2)+H,(window_size*2):(window_size*2)+W]

    new=255-new
    out = ApplyMask(new, mask)
    out = AdjustContrast(out)

    cv2.imwrite(image[:-4]+"__05Filtered.png", out * 255.0)

    return out

Preprocessar_imagen("diaretdb1_image001.png")
