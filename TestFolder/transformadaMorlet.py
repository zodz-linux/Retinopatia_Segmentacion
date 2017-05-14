#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np


class CVGaborProcessedImage(object):

    def __init__(self, scale, epsilon, theta, k0y):
        self.scale = scale
        self.epsilon = epsilon
        self.theta = theta
        self.k0y = k0y


    def generate(self, image):
        waveletSize = self.getIdealWaveletSize()
        (img_width, img_height) = image.shape
        dft_M = cv2.getOptimalDFTSize(img_height)
        dft_N = cv2.getOptimalDFTSize(img_width)

        # Generate the corresponding source image in the frequency domain
        dft_B = np.fft.fft2(image, [dft_M, dft_N])
        dft_B_shift = np.fft.fftshift(dft_B)

        # Apply the continuous wavelet transform for params:
        #     theta = 15 degrees, scale = 3.0, epsilon = 4.0, k0 = 3.0
        wavelet = self.morlet(waveletSize, waveletSize, self.theta,
            self.scale, self.epsilon, 0.0, self.k0y)

        # Generate the corresponding wavelet image in the frequency domain
        (wavelet_width, wavelet_height) = wavelet.shape
        dft_A = np.zeros((dft_M, dft_N), dtype='complex')
        yWaveletCentered = (dft_M - wavelet_height) / 2
        xWaveletCentered = (dft_N - wavelet_width) / 2
        dft_A[yWaveletCentered:yWaveletCentered + wavelet_height,
              xWaveletCentered:xWaveletCentered + wavelet_width] =\
            wavelet[0:wavelet_height, 0:wavelet_width]
        dft_A = np.fft.fft2(dft_A) #, [(wavelet_height + dft_M) / 2, (wavelet_width + dft_N) / 2])
        dft_A_shift = np.fft.fftshift(dft_A)

        # Multiply the source image and the wavelet image in the frequency domain
        current = np.zeros((dft_M, dft_N), dtype='complex')
        current = dft_B * np.conjugate(dft_A)
        # cv2.mulSpectrums(np.array(np.dstack([dft_B.real,dft_B.imag])),
        #                  np.array(np.dstack([dft_A.real, dft_A.imag])), 0,
        #                  np.array(np.dstack([current.real, current.imag])), conjB=True)


        # Apply the inverse fourier transform on the resulting image
        current = np.fft.ifft2(current, [dft_M, dft_N])

        return current


    def getIdealWaveletSize(self):
        '''Returns the ideal wavelet size for the current parameters'''

        size = 350
        wavelet = self.morlet(size, size, self.theta, self.scale, self.epsilon,
            0.0, self.k0y)

        i = 0
        j = 0
        countRows = 0
        (width, height) = wavelet.shape
        for i in xrange(height):
            modulus = 0.0
            for j in xrange(width):
                re = wavelet.real[i][j]
                im = wavelet.imag[i][j]

                modulus = np.sqrt(re*re + im*im)
                if modulus > 1e-7:
                    break

            if j == width:
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

            if i == height: 
                countCols += 1

            if modulus > 1e-7:
                break

        result = size
        if countRows < countCols:
            result -= 2 * countRows
        else:
            result -= 2 * countCols

        return result


    def morlet(self, width, height, theta, a, epsilon, horizFreq, vertFreq):
        ''' Builds the wavelet image.

        PARAMETERS
        width: Width of the wavelet image
        height: Height of the wavelet image
        theta: The angle parameter (radians)
        a: The scale parameter
        epsilon: The epsilon parameter
        horizFreq: The horizontal frequency parameter
        vertFreq: The vertical frequency parameter

        RETURNS
        The resulting image.'''

        complexMorlet = np.zeros((width, height), dtype=np.complex)

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
