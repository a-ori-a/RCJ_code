import image
import cv2
from time import sleep

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No camera found")
    exit()

while True:
    ret, frame = cap.read()
    gray = image.gray(frame)
    hsv = image.hsv(frame)
    centers = []
    new = []
    for i in range(350,471,30):
        centers.append(image.detect_line(gray, i))
    
    for i in range(350,471,30):
        new.append(image.detect_by_hsv(hsv, i,frame))
    
    for i,j in enumerate(range(350, 441, 30)):
        cv2.line(frame,(centers[i],j), (centers[i+1],j+30), (255,255,255),thickness=3)
    for i,j in enumerate(range(350, 441, 30)):
        cv2.line(frame,(new[i],j), (new[i+1],j+30), (123,223,121),thickness=3)
    cv2.imshow("display", frame)
    key = cv2.waitKey(30)
    if key == 113:
        break
    elif key == 115: # press S
        cv2.imwrite("./photo.jpg", frame)