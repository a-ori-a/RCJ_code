import cv2
import image

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
hsv = image.hsv(frame)

x = y = 0

while True:
    if (point := image.is_color(hsv, x, y)) == 'green':
        color = (255,0,0)
    elif point == 'white':
        color = (255,255,255)
    else:
        print('black')
        color = (0,0,0)
    pic = cv2.circle(hsv,(x,y),5,color,-1)
    cv2.imshow('is_color_tester', pic)
    key = cv2.waitKey(30)
    print(key)