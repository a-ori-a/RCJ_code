import cv2
import image
import calculation
import intersection

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = image.hsv(frame)
    top = image.detect_line(hsv, 380)
    bottom = image.detect_line(hsv, 460)
    
    print(top, bottom)