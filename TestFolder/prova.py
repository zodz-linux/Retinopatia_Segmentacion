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

scale = 3.0;
epsilon = 4.0;
theta = np.pi / 12 # 15 degrees
k0y = 3.0;

cvgpi = CVGaborProcessedImage(scale, epsilon, theta, k0y)
wavelet = cvgpi.generate(out)
cv2.imshow("Morlet wavelet - Real part", wavelet.real)
cv2.imwrite("Morlet wavelet - Real part.png", wavelet.real)
cv2.waitKey(0)
cv2.imshow("Morlet wavelet - Imaginary part", wavelet.imag)
cv2.imwrite("Morlet wavelet - Imaginary part.png", wavelet.imag)
cv2.waitKey(0)

#mi_min = np.min(mi)
#mi_max = np.max(mi)
#mi = 255 * (mi - mi_min) / (mi_max - mi_min)
#mi = mi - np.min(mi)
#mi = mi / np.max(mi)
