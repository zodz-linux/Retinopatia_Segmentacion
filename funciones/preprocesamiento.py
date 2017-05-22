#!/usr/bin/python
import cv2
import numpy as np

def build_filters():
    filters = []
    ksize = 10
    for theta in np.arange(0, 165, 30):
        kern = cv2.getGaborKernel((ksize, ksize), 5.0, theta, 10.0, 1.5, 0.2, ktype=cv2.CV_32F)
        kern /= 1.4*kern.sum()
        filters.append(kern)
    return filters

def process(img, filters):
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        np.maximum(accum, fimg, accum)
    return accum

def ApplyMask(image):
    mask = cv2.imread('mask1.png') #cargar mascara
    mask = mask[:, :, 1]    # Load mask
    #image = image[:, :, 1]  # Take green layer
    img2 = image.copy()
    img2 = 255 - img2
    img = cv2.bitwise_and(img2, img2, mask = mask) # Maskingaxxxxxxx
    return img

def preprocesar(img):
    mask1 = cv2.imread('mask1.png') #cargar mascara
    mask2 = cv2.imread('mask2.png') #cargar mascara
    mask1 = mask1[:,:,1]
    mask2 = mask2[:,:,1]
    img = (255-img)               #aplicar negativo
    filters = build_filters()     #construir filtro
    img =ApplyMask(img,mask1)     #enmascarar imagen
    img = process(img, filters)  #Aplica el  filtro
    img = ApplyMask(img,mask2)   #enmascarar imagen
    return img
