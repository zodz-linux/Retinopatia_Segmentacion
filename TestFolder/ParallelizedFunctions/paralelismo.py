import multiprocessing
import numpy as np
import cv2
import thread
import os

"""
The multiprocessing library provides the Pool class for simple parallel processing tasks.
The Pool class has the following methods:
"""

OutPath=(os.getcwd()+"/Output/")

def BorderExtensorMatrix(Image,BorderExtension=1):
    H,W=Image.shape #obtiene las dimensiones de la  matriz
    Matriz=np.zeros(((H+(BorderExtension*2)),(W+(BorderExtension*2))),dtype=int)
    Matriz[BorderExtension:H+BorderExtension,BorderExtension:W+BorderExtension]=Image.copy()
    return  Matriz

def UsingMultiprocessing(function,listArgs):
    """ Using the multiprocessing module  python share data and function"""
    Ncpus=multiprocessing.cpu_count()            #assigna el numero de  procesadores disponibles
    pool = multiprocessing.Pool(processes=Ncpus) #crea un objeto multiprocesador con Ncpus
    pool_outputs = pool.map(function,listArgs )  #mapea la function en la lista de argumentos
    pool.close() #cierra (bloquea) el objeto pool
    pool.join()  #mantiene el bloqueo hasta la terminacion de los procesos
    return pool_outputs

def FastThresholding_v1(image,threshold):
    """
    input: image (cv2 object , int)
    La idea es  usar indices logicos  en matrices de numpy
    """
    img=image.copy() #crear copia
    binaryM = (image > threshold).astype(np.int)# binarizar con condicion
    binaryM = 1-binaryM            # invertir binaria
    index=np.nonzero(binaryM)      # encontrar indices diferentes a cero
    img[index[0],index[1]]=0       # asignar ceros
    return img

def FastThresholding_v2(listArgs):
    """
    input: tupla (cv2 object , int )
    La idea es  usar indices logicos  en matrices de numpy
    """
    img       = listArgs[0]
    threshold = listArgs[1]
    binaryM= (img < threshold).astype(np.int)# identificar pixeles no necesarios
    index=np.nonzero(binaryM)              # encontrar indices diferentes a cero
    img[index[0],index[1]]=0               # asignar ceros
    return img

def Binarization(image):
    img       = image.copy()
    binaryM= (img > 0).astype(np.int)# binarizar con condicion
    return binaryM

def ParallelThresholding(image,low_threshold,upper_threshold):
    "Las tuplas protejen la integridad de los datos ya que son inmutables"
    images=tuple((image.copy(),t) for t in xrange(low_threshold,upper_threshold+1))
    outs=UsingMultiprocessing(FastThresholding_v2,images)
    return outs

def Skeletonize(img):
    """ OpenCV function to return a skeletonized version of img, a Mat object"""
    img = img.copy() # don't clobber original
    skel = img.copy()
    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    counter=0
    while counter <100:
        eroded = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)  #erosionar
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)#dilatacion
        temp  = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img[:,:] = eroded[:,:]
        counter+=1
    return skel

def WriteImages(images,label,increment):
    contador=250
    for i in images:
        cv2.imwrite(OutPath+label+str(contador)+".png",i)
        contador-=increment
    return

def FastExtremePoints(image):
    h,k=image.shape
    image2=np.zeros((h+2,k+2),dtype=np.int8)
    Iedge=image.copy()
    image2[1:h+1,1:k+1]=image
    index=np.nonzero(image2)              # encontrar indices diferentes a cero
    neighbors=[[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    for point in index:
        value=0.0
        for n in xrange(1,len(neighbors)):
            ii=image2[  point[0]+neighbors[n][0],point[1]+neighbors[n][1]]
            jj=image2[point[0]+neighbors[n-1][0],point[1]+neighbors[n-1][1]]
            value+=abs(int(ii)-int(jj))
        value*=.5
        if  value >=2:
            value=2
        elif value >= 1 and  value <=2:
            value =1
        Iedge[point[0]-1,point[1]-1]=np.int8(value)
    return  Iedge



def ParalellizedSegmentation(image):
    """" La idea es cretar  el proceso paralelo parallelo
    para cada valor del histograma
    input: image
    output: segmentate image
    """

    tvalues     = range(200,256)
    Iwavelets   = tuple((image.copy(),t) for t in tvalues)
    print "iniciando Umbralizacion. Inputs: ",len(Iwavelets),"imagenes"
    Ithresholds = UsingMultiprocessing(FastThresholding_v2,Iwavelets)
    print "iniciando Adelgazamiento. Inputs: ",len(Ithresholds),"imagenes"
    Iskels      = UsingMultiprocessing(Skeletonize,Ithresholds)
    print "iniciando Binarization. Inputs: ",len(Iskels),"imagenes"
    Ibinarys    = UsingMultiprocessing(Binarization,Iskels)

    #threshold             = Iwavelet.max() #inicializa el valor del umbral
    #Ivessel_past          = Thresholding(Iwavelet,threshold)
    #skel                  = Skeletonize(Ivessel_past)
    #binarized             = Binarization(skel,1)
    #ExtremizedPoints      = ExtremePoints(binarized)
    #Iedge_past            = RemoveShortSegments(ExtremizedPoints,41)
    print "Hecho!, Numero de matrices:",len(Ibinarys)
    return





img    = cv2.imread("tester.png",0)
ParalellizedSegmentation(img)
#outs=ParallelThresholding(img,150,200)
#WriteImages(outs,"umbral_",1)
#Skels=UsingMultiprocessing(Skeletonize,outs)
#WriteImages(Skels,"skels_",1)


print "\tHecho!"
