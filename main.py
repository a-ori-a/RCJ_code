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
    hsv = image.hsv(frame)
    top = image.detect_line(hsv, 380)
    bottom = image.detect_line(hsv, 475)
    top = [int(x) for x in top]
    bottom = [int(x) for x in bottom]
    frame = cv2.addWeighted(frame, 0.6, hsv, 0.4, 0)
    image.draw(frame, top, bottom)
    cv2.imshow("display", frame)
    key = cv2.waitKey(30)
    if key == 113:
        break
    elif key == 115: # press S
        cv2.imwrite("./photo.jpg", frame)