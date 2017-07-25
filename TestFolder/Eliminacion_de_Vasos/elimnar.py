import cv2


def eliminar_vasos(Ired_layer,Isegmented):
    H,W = Isegmented.shape
    for  i in xrange(H):
        for j in xrange (W):
            if Isegmented[i,j] > 0:
                Ired_layer[i,j]=0
    return Ired_layer

red_layer = cv2.imread("diaretdb1_image001.png")
red_layer = red_layer[:,:,1]
cv2.imwrite("capa_verde.png",red_layer)
segemented1= cv2.imread("diaretdb1_image001_155_.png",0)
segemented2= cv2.imread("diaretdb1_image001_166_.png",0)

eliminated=eliminar_vasos(red_layer,segemented1)
cv2.imwrite("vasos_eliminados1.png",eliminated)

eliminated=eliminar_vasos(red_layer,segemented2)
cv2.imwrite("vasos_eliminados2.png",eliminated)
