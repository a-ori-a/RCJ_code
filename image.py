import cv2
import pandas as pd

# imageの配列のイメージ  ←?
"""
[ クソデカ大かっこ

    [   なんとも言えないカッコ
        (
            それぞれのピクセルのやつ
        )
    ]
]
"""

def get_camera():
    global cap
    for i in range(2,9):
        cap = cv2.VideoCapture(i)
        if cap.isOpened() : break

def hsv(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return result

def gray(img):
    ret, result = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_OTSU)
    return result

def detect_line_grayscale(image, ypos, result=False):
    data = image[ypos]
    blacklist = pd.Series([x for x,y in enumerate(data) if y==0])
    while image[ypos][int(blacklist.mean())] != 0 and len(blacklist) > 10:
        blacklist = blacklist[blacklist.quantile(0.1)<blacklist][blacklist<blacklist.quantile(0.9)] 
    try:
        # these cause bugs when no black color is detected
        mean = int(blacklist.mean())
        std = 2*int(blacklist.std())
    except:
        # so set them to 0 for now
        mean = 0
        std = 0
    if type(result) != bool:
        try:
            cv2.circle(result, (mean, ypos), 8, (0,0,255), thickness=-1)
            cv2.circle(result, (mean-std, ypos), 8, (0,255,0), thickness=-1)
            cv2.circle(result, (mean+std, ypos), 8, (0,255,0), thickness=-1)
        except:
            pass
    return (mean)

def simple(img, ypos, result=False):
    data = pd.Series(img[ypos])
    left_side = 0
    right_side = 0
    if 0 in data:
        check_counter = 0
        while data[check_counter] == 255:
            check_counter += 1
        left_side = check_counter
        while data[check_counter] == 0 and check_counter < 639:
            check_counter += 1
        right_side = check_counter
    cv2.circle(img, (left_side, ypos), 10, (255,255,255), thickness=-1)
    cv2.circle(img, (right_side, ypos), 10, (255,255,255), thickness=-1)
    return int((left_side+right_side)/2)

"""
覚えておきましょう
H S V
↓ ↓ ↓ 
B G R
"""

def detect_line(img, ypos):
    data = [x[1] for x in img[ypos]]
    line_list = pd.Series([x for x,y in enumerate(data) if y > 100])
    if len(line_list) == 0:
        mean = 0
    else:
        mean = line_list.mean()
    return mean

def draw(img):
    cv2.rectangle(img, (120, 200), (520, 350), (12, 200, 56), thickness=2)
    cv2.rectangle(img, (180, 380), (460, 475), (50, 100, 255), thickness=2)