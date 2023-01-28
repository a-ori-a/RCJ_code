import cv2
import image

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
frame = cv2.resize(frame,(200,480))
hsv = image.hsv(frame)

x = y = 0

while True:
    if (point := image.is_color(hsv, x, y)) == 'green':
        color = (0,255,0)
    elif point == 'white':
        color = (255,255,255)
    else:
        print('black')
        color = (0,0,0)
    pic = frame
    cv2.circle(pic,(x,y),5,color,-1)
    cv2.imshow('is_color_tester', pic)
    key = cv2.waitKey(30)
    # print(key)
    if key == 81:
        x = max(0,x-3)
    elif key == 82:
        y = max(0,y-3)
    elif key == 83:
        x = min(199,x+3)
    elif key == 84:
        y = min(479, y+3)
    elif key == 113:
        exit()
