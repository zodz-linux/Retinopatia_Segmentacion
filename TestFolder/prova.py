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

img = cv2.imread('imagen1.png')
mask = cv2.imread('mask.png')   # Load mask
out = ApplyMask(img, mask)
cv2.imwrite("enmascaradaEinvertida.png", out)

scale = 4.0
epsilon = 4.0
k0y = 3.0

cvgpi = CVGaborProcessedImage(scale, epsilon, k0y)
wavelet = cvgpi.generate(out)
cv2.imshow("Morlet wavelet - Real part", wavelet.real)
cv2.imwrite("Morlet wavelet - Real part.png", wavelet.real)
cv2.waitKey(0)
#print('Min = ', np.min(wavelet.real))
#print('Max = ', np.max(wavelet.real))
cv2.imshow("Morlet wavelet - Imaginary part", wavelet.imag)
cv2.imwrite("Morlet wavelet - Imaginary part.png", wavelet.imag)
cv2.waitKey(0)
