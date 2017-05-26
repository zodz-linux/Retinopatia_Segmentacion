import cv2
import numpy as np
from transformadaMorlet import CVGaborProcessedImage


def ApplyMask(image, mask):
    mask = mask[:, :, 1]    # Load mask
    image = image[:, :, 1]  # Take green layer
    img2 = image.copy()
    img2 = 255 - img2
    img = cv2.bitwise_and(img2, img2, mask = mask) # Maskingaxxxxxxx
    return img

img = cv2.imread('diaretdb1_image003.png')
#img = cv2.imread('02_test.tif')
mask = cv2.imread('mask.png')   # Load mask
#mask = cv2.imread('02_test_mask.png')
out = ApplyMask(img, mask)
cv2.imwrite("enmascaradaEinvertida.png", out)


#maski = cv2.imread('maski.png')   # Load inverted mask
#maski = (maski[:, :, 0] + maski[:, :, 1] + maski[:, :, 2]) / 3.0
#out = out + maski
#cv2.imwrite("Con-maski.png", out)


scale = 8.0
epsilon = 4.0
k0y = 3.0
out = out / 255.0
cvgpi = CVGaborProcessedImage(scale, epsilon, k0y)
wavelet = cvgpi.generate(out)
print('Min = {}, max = {}'.format(np.min(wavelet.real), np.max(wavelet.real)))
cv2.imwrite("Morlet wavelet - Real part.png", wavelet.real * 255.0)
