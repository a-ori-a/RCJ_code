import cv2
import image

cap = cv2.VideoCapture(0)

count = 26
while True:
    ret, frame = cap.read()
    frame = image.hsv(frame)
    cv2.imshow("stream", frame)
    key = cv2.waitKey(30)
    if key == 115: # press S
        cv2.imwrite("./pic/"+str(count)+".jpg", frame)
        count += 1
    elif key == 113: # press Q
        exit()