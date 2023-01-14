import cv2
from time import sleep
from concurrent.futures import ProcessPoolExecutor
import image
import intersection
import calculation

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
    bottom = image.detect_line(hsv, 460)

    points = []
    for i in [200, 275, 350]:
        points.append(image.detect_line(hsv, i))

    cv2.putText(frame, "turn_strength : "+str(calculation.turn_strength(top[0], bottom[0])), (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (12,255,0), thickness=2)
    cv2.putText(frame, intersection.intersection(points), (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (12, 255, 0), thickness=2)

    frame = cv2.addWeighted(frame, 0.6, hsv, 0.4, 0)
    image.draw(frame, [top, bottom], points)
    cv2.imshow("hsv", hsv)
    cv2.imshow("display", frame)
    key = cv2.waitKey(30)
    if key == 113:
        break
    elif key == 115: # press S
        cv2.imwrite("./photo.jpg", frame)
#test ~futon ga futtobanakatta~