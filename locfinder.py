import cv2
from cv2 import cv
import fileinput
import sys


vc = cv2.VideoCapture('foo')
vc.set(cv.CV_CAP_PROP_FOURCC, cv.CV_FOURCC('h','2','6','4'))

while True:
    ret, frame = vc.read()
    if frame:
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
