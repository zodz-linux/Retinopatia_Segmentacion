import cv2
import numpy as np

def main(file_name,window_size=12,umbral=11,iterations=20):
    # variables creation
    img=cv2.imread(file_name)
    img=img[:,:,1] # green  layer
    W,H=img.shape
    reading_image=np.zeros((W+(window_size*4),H+(window_size*4)),dtype=np.int)
    reading_image[(window_size*2):(window_size*2)+W,(window_size*2):(window_size*2)+H]=img
    writing_image=reading_image.copy()
    W,H=reading_image.shape
    # variables creation


    neighbors=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    # mark  edge
    for it in xrange(iterations):
        for  i in xrange(W):
            for j in xrange(H):
                if reading_image[i,j] > umbral:
                    for p in [[1,0],[0,1],[-1,0],[0,-1]]:
                        if reading_image[p[0]+i,p[1]+j] < umbral:
                            writing_image[p[0]+i,p[1]+j]=-1
        reading_image=writing_image.copy()
        # marked  edge
        for  i in xrange(W):
            for j in xrange(H):
                if reading_image[i,j]== -1:
                    not_nulls=0   # count not null values
                    local_value=0 # it will be the mean value
                    for p in  neighbors:
                        if reading_image[i+p[0],j+p[1]] > umbral:
                            not_nulls+=1
                            local_value+=reading_image[i+p[0],j+p[1]]
                    local_value/=float(not_nulls)
                    writing_image[i,j]=local_value
        reading_image=writing_image.copy()

    cv2.imwrite("out.png",reading_image)
    pass


main("imagen_tester.png")
