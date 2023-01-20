import cv2
import image

# how to detect intersection
# fot each (top, center, bottom), judge (left, center, right) and then integrate the answer
# switch by the combined chars

def around(standard, num, thresh=10):
    if abs(num - standard) < thresh:
        return 0
    elif num < standard:
        return -1
    elif num > standard:
        return 1
    else:
        print("Something wrong happened in intersection detection")
        return 0

def intersection(points: list):
    result = ""
    for point in points:
        condition = around(320, point[0], 80)
        if condition == 0:
            result  += "c"
        elif condition == -1:
            result += "l"
        elif condition == 1:
            result += "r"
    if result == "clc":
        return "left"
    elif result == "crc":
        return "right"
    else:
        return "straight"

def intersection(img):
    img = cv2.rotate(img, cv2.ROTATE_90_CONTERCLOCKWISE)
    img = img[200:480, 0:100]
    # 画像を左向きに90°回転させてimage.pyで作ったdetect_lineを適応できるようにした
    # 関数を乱用してる感じはするけどこっちのほうが効率としては上なはず
    # the result will be
    # 0 --- 280
    # ||---
    # 100
    edges = [image.detect_line(img, i) for i in (10, 90)]
    # edges[0] --> right,  edges[1] --> left
    # 条件がかなり緩いから本番環境でしきい値とらないといけない
    # たぶん値が小さい時　= 上の方にある時は無視するみたいな感じのコードでやっていくと良いんじゃないでしょうか
    # --> 結局しきい値を設定してやっそれ以下なら緑として認めないような仕組みを採用
    threash = 280
    right_green = edges[0] > threash
    left_geen = edges[1] > threash
    if not (right_green or left_green):
        return "white" # go straight
    elif left_green and right_green:
        return "cross"
    elif not left_green and right_green:
        return "right"
    elif left_green and right_green:
        return "left"
