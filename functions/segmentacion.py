import os
import numpy as np
import  cv2
from preprocesamiento import *

def skeletonize(img):
    """ OpenCV function to return a skeletonized version of img, a Mat object"""
    img = img.copy() # don't clobber original
    skel = img.copy()
    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    counter=0
    while counter <100:
        eroded = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel) #apertura
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
        temp  = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img[:,:] = eroded[:,:]
        counter+=1
    return skel

def Binarization(image,threshold):
    high,width=image.shape
    for i in xrange(high):
        for j in xrange(width):
            tmp=image[i,j]
            if tmp < 0:
                print "Error"
                break
            elif tmp >=threshold:
                image[i,j]=1
            else:
                image[i,j]=0
    return image

def Binary2Maximize(image):
    threshold=1
    high,width=image.shape
    for i in xrange(high):
        for j in xrange(width):
            tmp=image[i,j]
            if tmp < 0:
                print "Error"
                break
            elif tmp >=threshold:
                image[i,j]=150
            else:
                image[i,j]=0
    return image

def Thresholding(image,threshold):
    high,width=image.shape
    binary_image=image.copy()
    for i in xrange(high):
        for j in xrange(width):
            tmp=image[i,j]
            if tmp < 0:
                print "Error"
                break
            elif tmp >=threshold:
                binary_image[i,j]=image[i,j]
            else:
                binary_image[i,j]=0
    return binary_image

def ExtremePoints(image):
    h,k=image.shape
    image2=np.zeros((h+2,k+2),dtype=np.int8)
    Iedge=image.copy()
    image2[1:h+1,1:k+1]=image
    points=[[i,j] for i in xrange(1,h+1) for j in xrange(1,k+1) ]
    neighbors=[[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    for point in points:
        if image2[point[0],point[1]] == 0:
            continue #Do not do it if not vessel pixel
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

def RemoveInWindow(subm):
    # m is submatrix at image
    #seed is the central pixel in submatrix
    h,k=subm.shape
    seed=[h/2,k/2]
    count=0
    for i in xrange(h):
        for j in xrange(k):
            if subm[i,j]==1:
                count+=1
    if count >= 2:
        m=np.zeros((h+2,k+2),dtype=np.int8)
        m[1:h+1,1:k+1]=subm
        seed[0]+=1
        seed[1]+=1
        neighbors=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
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
    if w%2 == 0 or  w < 3:
        print "Error, Length window is not compatible "
        return image
    h,k=image.shape
    img=np.zeros((h+(2*border),k+(2*border)),dtype=np.int8)
    img[border:(h+border),border:(k+border)]=image[:,:]
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

    #CalculateDifference(I_i_segmented,I_j_segmented,mask,threshold)
def CalculateDifference(image_i,image_j,image_mask,threshold,MinDiff=2):
    h,k=image_i.shape
    DiferentPoints=[] # difference  pixels
    for i  in xrange(h):
        for j in xrange(k):
            if image_i[i,j] != 0 and 0 != image_j[i,j]:
                DiferentPoints.append([i,j])
    ContinueIteration=True
    if MinDiff >= len(DiferentPoints):
        ContinueIteration=False
        print "Criterio de paro: Diferencias minimas entre i,j"
        return image_mask, ContinueIteration
    else:
        for  p in DiferentPoints:
            image_mask[p[0],p[1]]=threshold
        return image_mask, ContinueIteration

def SingleSegmentation(imagex):
    img = cv2.imread("Images/"+imagex) # read file
    image= preprocesar(img) #preprocesar
    threshold=image.max() #inicializar umbral
    thresholded = Thresholding(image,threshold)
    print "\tUmbral Actual: ",threshold
    mask=thresholded.copy()
    skel=skeletonize(thresholded)
    binary = Binarization(skel,1)
    ep=ExtremePoints(binary)
    I_i_segmented=RemoveShortSegments(ep,11)
    threshold=threshold-1
    ContinueIteration=True
    iteracion=1
    while True:
        serie=str(iteracion)
        if iteracion < 10:
            serie="00"+str(iteracion)
        if iteracion > 9 and iteracion< 100 :
            serie="0"+str(iteracion)
        cv2.imwrite("OutputImages/ByThreshold/"+imagex[:-4]+"_"+serie+".png",mask)
        print "\t\t Iteracion: ",iteracion
        print "\tUmbral Actual: ",threshold
        thresholded = Thresholding(image,threshold)
        skel=skeletonize(thresholded)
        binary = Binarization(skel,1)
        ep=ExtremePoints(binary)
        I_j_segmented=RemoveShortSegments(ep,11)
        mask,ContinueIteration=CalculateDifference(I_i_segmented,I_j_segmented,mask,threshold,5)
        threshold=threshold-1
        iteracion+=1
        if not(ContinueIteration) or (threshold==0):
            print "ContinueIteration: ",ContinueIteration
            print "Umbral:            ",threshold
            return mask
        I_i_segmented=I_j_segmented.copy()
