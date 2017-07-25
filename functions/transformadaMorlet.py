#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np


class CVGaborProcessedImage(object):

    def __init__(self, scale, epsilon, k0y):
        self.scale = scale
        self.epsilon = epsilon
        self.k0y = k0y


    def generate(self, image):
        waveletSize = self.getIdealWaveletSize()
        (img_height, img_width) = image.shape
        dft_M = cv2.getOptimalDFTSize(img_height)
        dft_N = cv2.getOptimalDFTSize(img_width)

        # Generate the corresponding source image in the frequency domain
        dft_B = np.fft.fft2(image, [dft_M, dft_N])

        current = np.zeros((dft_M, dft_N), dtype='complex')

        # Apply the continuous wavelet transform
#        maximum = np.zeros((dft_M, dft_N), dtype='float32')
#        iMaximum = np.zeros((dft_M, dft_N), dtype='float32')

        maximum = np.finfo(np.float32).min * \
                  np.ones((dft_M, dft_N), dtype='float32')
        iMaximum = np.zeros((dft_M, dft_N), dtype='float32')

        for multiplier in xrange(18):

            # Generate the wavelet complex image
            angle = multiplier * 10.0 # in degrees
            print "\x1b[1A"+"\x1b[2K",#solo elimina una linea del std out
            print('\t*Morlet (scale = {}, epsilon = {}, theta = {}, k0 = [0, {}])'.
                  format(self.scale, self.epsilon, angle, self.k0y))

            wavelet = self.morlet(waveletSize, waveletSize, angle,
                self.scale, self.epsilon, 0.0, self.k0y)

            # Generate the corresponding wavelet image in the frequency domain
            (wavelet_height, wavelet_width) = wavelet.shape
            dft_A = np.zeros((dft_M, dft_N), dtype='complex')
            yWaveletCentered = (dft_M - wavelet_height) / 2
            xWaveletCentered = (dft_N - wavelet_width) / 2
            dft_A[yWaveletCentered:yWaveletCentered + wavelet_height,
                  xWaveletCentered:xWaveletCentered + wavelet_width] =\
                  wavelet[0:wavelet_height, 0:wavelet_width]
            dft_A = np.fft.fft2(dft_A)

            # Multiply the source image and the wavelet image in the frequency domain
            current = dft_B * np.conjugate(dft_A)

            # Apply the inverse fourier transform on the resulting image
            iCurrent = np.fft.ifft2(current, [dft_M, dft_N])

            # Create the resulting feature image
            (current_height, current_width) = current.shape
            for i in xrange(current_height):
                for j in xrange(current_width):
                    iCurrent[i][j] /= self.scale
#                    iCurrent[i][j].real = (iCurrent[i][j].real / self.scale)
#                    iCurrent[i][j].imag = (iCurrent[i][j].imag / self.scale)
                    re = iCurrent[i][j].real
                    im = iCurrent[i][j].imag

                    # Calculate the modulus of this pixel
                    iCurrent[i][j] = np.sqrt(re*re + im*im) + 0.j
#                    iCurrent[i][j].real = sqrt(re*re + im*im)
#                    iCurrent[i][j].imag = 0.0

                    # Store the maximum of the modulus on this pixel
                    if iCurrent[i][j].real > iMaximum[i][j]:
                        iMaximum[i][j] = iCurrent[i][j].real


        # Shifts the resulting image to obtain the correct image
        iMaximum = np.fft.fftshift(iMaximum)

        # Extract the region of interest from the result of the transform
        iMaximum = iMaximum[0:img_height, 0:img_width]

        return iMaximum


    def getIdealWaveletSize(self):
        '''Returns the ideal wavelet size for the current parameters'''

        size = 350
        wavelet = self.morlet(size, size, 45.0, self.scale, self.epsilon,
            0.0, self.k0y)

        i = 0
        j = 0
        countRows = 0
        (height, width) = wavelet.shape
        for i in xrange(height):
            modulus = 0.0
            for j in xrange(width):
                re = wavelet.real[i][j]
                im = wavelet.imag[i][j]

                modulus = np.sqrt(re*re + im*im)
                if modulus > 1e-7:
                    break

            if j == width-1:
                countRows += 1

            if modulus > 1e-7:
                break

        countCols = 0
        for j in xrange(width):
            modulus = 0.0
            for i in xrange(height):
                re = wavelet.real[i][j]
                im = wavelet.imag[i][j]

                modulus = np.sqrt(re*re + im*im)
                if modulus > 1e-7:
                    break

            if i == height-1:
                countCols += 1

            if modulus > 1e-7:
                break

        result = size
        if countRows < countCols:
            result -= 2 * countRows
        else:
            result -= 2 * countCols

        return result


    def morlet(self, width, height, angle, a, epsilon, horizFreq, vertFreq):
        ''' Builds the wavelet image.

        PARAMETERS
        width: Width of the wavelet image
        height: Height of the wavelet image
        angle: The angle parameter (degrees)
        a: The scale parameter
        epsilon: The epsilon parameter
        horizFreq: The horizontal frequency parameter
        vertFreq: The vertical frequency parameter

        RETURNS
        The resulting image.'''

        complexMorlet = np.zeros((width, height), dtype='complex64')
        theta = np.pi * angle / 180.0;

        W = width / 2
        H = height / 2
        for y in xrange(-H, H):
            for x in xrange(-W, W):
                xValue = np.zeros(2, dtype='float32')
                yValue = np.zeros(2, dtype='float32')

                xValue[1] = (x * np.cos(-theta)) - (y * np.sin(-theta))
                yValue[1] = (x * np.sin(-theta)) + (y * np.cos(-theta))

                xValue[1] /= a
                yValue[1] /= a

                scaledX = xValue[1]
                scaledY = yValue[1]

                xValue[1] *= horizFreq
                yValue[1] *= vertFreq

                complexMorlet.real[y + H][x + W] = np.cos(xValue[1] + yValue[1])
                complexMorlet.imag[y + H][x + W] = np.sin(xValue[1] + yValue[1])

                elongatedX = scaledX * np.power(epsilon, -0.5)

                gaussian2d = np.exp((-0.5) * (np.power(elongatedX, 2.0) +
                    np.power(scaledY, 2.0)))

                complexMorlet.real[y + H][x + W] *= gaussian2d
                complexMorlet.imag[y + H][x + W] *= -gaussian2d

        return complexMorlet
