import image
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret,img = cap.read()
    hsv = image.hsv(img)
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    image.detect_by_hsv(hsv,300,img)
    new = []
    for i in range(350,471,30):
        new.append(image.detect_by_hsv(img, i,img))
    for i,j in enumerate(range(350, 441, 30)):
        cv2.line(img,(new[i],j), (new[i+1],j+30), (123,223,121),thickness=3)
    
    cv2.imshow("img", img)
    key = cv2.waitKey(40)
    if key == 113:
        break
    elif key == 115: # press S
        cv2.imwrite("./photo.jpg", hsv)