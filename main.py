import image
import cv2
from time import sleep

# resolution 640x480
# 1  ~~~  640
# ...
# 480

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No camera found")
    exit()

while True:
    ret, frame = cap.read()
    gray = image.gray(frame)
    hsv = image.hsv(frame)

    image.draw(frame)
    cv2.imshow("display", frame)
    key = cv2.waitKey(30)
    if key == 113:
        break
    elif key == 115: # press S
        cv2.imwrite("./photo.jpg", frame)