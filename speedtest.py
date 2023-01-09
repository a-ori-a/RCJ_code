import cv2
from time import time

cap = cv2.VideoCapture(0)

def timedelta():
    start = time()
    for i in range(100):
        ret, frame = cap.read()
    return time() - start

print(timedelta())