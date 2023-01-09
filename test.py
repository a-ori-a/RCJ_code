import cv2
import image
import numpy as np
import pandas as pd
from time import sleep
import intersection

#カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)

# resolution 640x480
# 1  ~~~  640
# ...
# 480

while True:
    ret, frame = cap.read()
    hsv = image.hsv(frame)
    frame = intersection.horizontal(frame)
    cv2.imshow("Test",frame)
    cv2.waitKey(100)

def detect_line_2nd(data, ypos):
    blacklist = [x for x,y in enumerate(data) if y==0]
    something = pd.Series(blacklist)
    min, max = something.quantile([0.4,0.6])
    something = something[min<something][something<max]
    mean = int(something.mean())
    std = 2*int(something.std())
    try:
        cv2.circle(frame, (mean, ypos), 8, (0,0,255), thickness=-1)
        cv2.circle(frame, (mean-std, ypos), 8, (0,255,0), thickness=-1)
        cv2.circle(frame, (mean+std, ypos), 8, (0,255,0), thickness=-1)
    except:
        pass
    return (mean, ypos)

def initialize():
    ret, frame = cap.read()
    ret, gray = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 128, 256, cv2.THRESH_OTSU)
    tmp = [x for x,y in enumerate(gray[400]) if y == 0]
    tmp = pd.Series(tmp)
    std = tmp.std()
    return std*2

def detect_line(data, ypos):
    blacklist = [x for x,y in enumerate(data) if y==0]
    something = pd.Series(blacklist)
    while abs(something.std()*2-line_width) > 20:
        something = something[something.quantile(0.05)<something][something<something.quantile(0.95)]
    try:
        # these cause bugs when no black color detected
        mean = int(something.mean())
        std = 2*int(something.std())
    except:
        # so we set them to 0 for the time being
        mean = 0
        std = 0
    try:
        cv2.circle(frame, (mean, ypos), 8, (0,0,255), thickness=-1)
        cv2.circle(frame, (mean-std, ypos), 8, (0,255,0), thickness=-1)
        cv2.circle(frame, (mean+std, ypos), 8, (0,255,0), thickness=-1)
    except:
        pass
    return (mean, ypos)




def detect_line_old(data, ypos):
    blacklist = [x for x,y in enumerate(data) if y==0]
    something = pd.Series(blacklist)
    try:
        mean = int(something.mean())
        std = 2*int(something.std())
    except:
        mean = 0
        std = 0
    # try:
    #     cv2.circle(frame, (mean, ypos), 8, (0,0,255), thickness=-1)
    #     cv2.circle(frame, (mean-std, ypos), 8, (0,255,0), thickness=-1)
    #     cv2.circle(frame, (mean+std, ypos), 8, (0,255,0), thickness=-1)
    # except:
    #     pass
    return (mean, ypos)

line_width = initialize()

while True:
    ret, frame = cap.read()
    ret, gray = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 128, 256, cv2.THRESH_OTSU)
    btm = detect_line(gray[470], 470)
    top = detect_line(gray[400], 400)
    try:
        cv2.arrowedLine(frame, btm, top, (255,0,0),thickness=5, tipLength=0.4)
    except:
        pass
    btm = detect_line_old(gray[470], 470)
    top = detect_line_old(gray[400], 400)
    try:
        cv2.arrowedLine(frame, btm, top, (255,255,255),thickness=5, tipLength=0.4)
    except:
        pass
    cv2.imshow("test", frame)
    cv2.waitKey(30)
for i in gray[399]:
    print(int(i/255))


    # for vt in range(399,479, 10):
    #     readLine = gray[vt]
    #     # gray = np.array([gray])
    #     for i, x in enumerate(readLine):
    #         if not x:
    #             cv2.circle(frame, (i,vt), 1, (0,0,255), thickness=-1)
    #         else:
    #             pass
    # cv2.imshow("result", frame)
    # cv2.waitKey(33)
    


exit()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 128, 192,cv2.THRESH_OTSU)
    cv2.imshow("frame", frame)
    # cv2.imshow("gray", gray)
    cv2.waitKey(30)