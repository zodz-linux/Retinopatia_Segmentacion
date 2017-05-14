import cv2


def GetHuMoments(matrix):
    atribbutes=cv2.HuMoments(cv2.moments(matrix))
    return atribbutes
