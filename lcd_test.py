import cv2
import image
import calculation
import intersection
from lcd import lcd

cap = cv2.VideoCapture(0)
display = lcd()

while True:
    ret, frame = cap.read()
    hsv = image.hsv(frame)
    top = image.detect_line(hsv, 380)
    bottom = image.detect_line(hsv, 460)
    points = []
    for i in [200, 275, 350]:
        points.append(image.detect_line(hsv, i))

    state = intersection.intersection(points)
    # print(state)
    # lcd.setCursor(0,0)
    # lcd.printout(state.center(16))
    # lcd.setCursor(0, 1)
    # lcd.printout((str(top[0]) + ", " + str(bottom[0])).center(16))
    
    # print(top[0], bottom[0])
    display.show(state, 0)
    display.line_indicator(bottom[0])