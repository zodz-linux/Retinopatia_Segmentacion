import multiprocessing
import numpy as np
import cv2
import thread
import os

"""
The multiprocessing library provides the Pool class for simple parallel processing tasks.
The Pool class has the following methods:
"""
def BorderExtensorMatrix(Image,BorderExtension=1):
    H,W=Image.shape #obtiene las dimensiones de la  matriz
    Matriz=np.zeros(((H+(BorderExtension*2)),(W+(BorderExtension*2))),dtype=int)
    Matriz[BorderExtension:H+BorderExtension,BorderExtension:W+BorderExtension]=Image.copy()
    return  Matriz

def FastThresholding_v1(image,threshold):
    """
    input: image (cv2 object , int)
    La idea es  usar indices logicos  en matrices de numpy
    """
    img=image.copy() #crear copia
    binaryM = (image < threshold).astype(np.int)# binarizar con condicion
    index=np.nonzero(binaryM)     # encontrar indices diferentes a cero
    img[index[0],index[1]]=0      # asignar ceros
    return img

def Binarization(image,threshold=0):
    img       = image.copy()
    binaryM= (img > threshold).astype(np.int)# binarizar con condicion
    return binaryM

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

def WriteImage(image,label):
    cv2.imwrite((os.getcwd()+"/Output/")+label+".png",image)
    return

def MarkExtremePoints(image):
    h,k=image.shape #tomar las dimensiones
    Imarked=image.copy()
    CopyImage=np.zeros((h+2,k+2),dtype=np.int8)
    CopyImage[1:h+1,1:k+1]=image
    index=np.nonzero(CopyImage)   # encontrar indices diferentes a cero
    neighbors=[[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    for i in xrange(len(index[0])):
        point=(index[0][i],index[1][i])
        value=0.0 #iniciando el valor de la suma
        for n in xrange(1,len(neighbors)):
            term1=CopyImage[point[0]+neighbors[n][0]   , point[1]+neighbors[n][1]]
            term2=CopyImage[point[0]+neighbors[n-1][0] , point[1]+neighbors[n-1][1]]
            value+=abs(int(term1)-int(term2))
        value=int(value/2.)
        #print value
        """
        Aqui las condiciones hacen mas sensible la identificacion de bordes
        es por eso que solo en caso  de que  el promedio de la suma de los vecinos
        sea 2   se identifica como borde. cualquier valor superior se toma como
        bixel intermedio y no borde
        """
        if  value >1:
            value=2
            Imarked[point[0]-1,point[1]-1]=np.int8(value) #Marcando  extremos
        #else:
        #    value =1
        #Imarked[point[0]-1,point[1]-1]=np.int8(value) #Marcando  extremos
    return  Imarked


def RemoveInWindow(subm):
    # m is submatrix at image
    #seed is the central pixel in submatrix
    h,k=subm.shape
    seed=[h/2,k/2]
    count=0
    neighbors=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    m=np.zeros((h+2,k+2),dtype=np.int8)
    m[1:h+1,1:k+1]=subm

    binaryM = (image == 1 ).astype(np.int)# binarizar con condicion
    index=np.nonzero(binaryM)   # encontrar indices differentes

    if len(index)>2:
        seed[0]+=1
        seed[1]+=1
        Tree=[]#initTree
        for node in  neighbors:
            if (m[seed[0]+node[0],seed[1]+node[1]]) != 0:
                Tree.append([[seed[0]+node[0],seed[1]+node[1]]])
        search =True
        while search:
            search=False
            for i in xrange(len(Tree)):
                leaf=Tree[i][-1] #Temporal node
                if m[leaf[0],leaf[1]] == 1:
                    continue
                for node in neighbors:
                    current=[leaf[0]+node[0],leaf[1]+node[1]]
                    if current == seed:
                        continue
                    elif current in  Tree[i]:
                        continue
                    elif (m[current[0],current[1]]) != 0:
                        Tree[i].append(current)
                        search=True
        Candidate=[]
        for path in Tree:
            tmp=path[-1]
            if m[tmp[0],tmp[1]] == 1:
                t=[[n[0]-1,n[1]-1] for n in path]
                Candidate+=t
        seed[0]-=1
        seed[1]-=1
        Candidate.append(seed)
        for coord in Candidate:
            subm[coord[0],coord[1]]=0
    return  subm

def RemoveShortSegments(image,w=5):
    border=w/2
    if  w < 5:
        return image
    if w%2 == 0 :
        w+=1
    h,k=image.shape
    #crear  matriz  con el  borde  expandido
    img=np.zeros((h+(2*border),k+(2*border)),dtype=np.int8)
    img[border:(h+border),border:(k+border)]=image[:,:]

    binaryM = (image == 2 ).astype(np.int)# binarizar con condicion
    ValuesX,ValuesY=np.nonzero(binaryM)   # encontrar indices diferentes a cero

    for aux in  xrange(len(ValuesX)):
        submatrix=img[ValuesX[aux]-border:(ValuesX[aux]+border+1),ValuesY[aux]-border:(ValuesY[aux]+border+1)]
        edges=[]
        for  a in xrange(w):
            for  b in xrange(w):
                if submatrix[a,b]==1:
                    edges.append([a,b])
        if len(edges) > 1 :
            for  p in edges:
                submatrix[p[0],p[1]]==0
            img[i-border:(i+border+1),j-border:(j+border+1)]=submatrix[:,:]


    # fin de la expancion
    for i in xrange(w/2,h+(w/2)):
        for j in xrange(w/2,k+(w/2)):
            if img[i,j] == 2:
                submatrix=img[i-border:(i+border+1),j-border:(j+border+1)]
                edges=[]
                for  a in xrange(w):
                    for  b in xrange(w):
                        if submatrix[a,b]==1:
                            edges.append([a,b])
                if len(edges) > 1 :
                    for  p in edges:
                        submatrix[p[0],p[1]]==0
                    img[i-border:(i+border+1),j-border:(j+border+1)]=submatrix[:,:]
            else:
                continue

    for i in  xrange(h):
        for j in xrange(k):
            if image[i,j] ==1:
                submatrix=img[i-border:(i+border+1),j-border:(j+border+1)]
                img[i-border:(i+border+1),j-border:(j+border+1)]=RemoveInWindow(submatrix)
    return image





def Segmentation(image):
    """"
    input: image open cv
    output: segmentate image
    """
    threshold    = 180#image.max()
    Iwavelet     = image.copy()
    Ithresholded = FastThresholding_v1(Iwavelet,threshold)
    WriteImage(Ithresholded,"umbralizada")
    Ithin        = Skeletonize(Ithresholded)
    Ibinary      = Binarization(Ithin)
    Imarks       = MarkExtremePoints(Ibinary)
    WriteImage(Imarks*200,"marcadores")
    #Iedge        = RemoveShortSegments(Imarks)
    print "Hecho!"
    return

img    = cv2.imread("tester.png",0)
Segmentation(img)
