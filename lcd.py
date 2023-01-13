import cv2
import image
import calculation
import intersection
import RGB1602

cap = cv2.VideoCapture(0)
lcd = RGB1602.RGB1602(16,2)

while True:
    ret, frame = cap.read()
    hsv = image.hsv(frame)
    top = image.detect_line(hsv, 380)
    bottom = image.detect_line(hsv, 460)
    points = []
    for i in [200, 275, 350]:
        points.append(image.detect_line(hsv, i))

    state = intersection.intersection(points)
    print(state)
    
    print(top[0], bottom[0])