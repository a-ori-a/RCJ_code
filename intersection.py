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

def intersection_old(points: list):
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
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # 画像を左向きに90°回転させてimage.pyで作ったdetect_lineを適応できるようにした
    # 関数を乱用してる感じはするけどこっちのほうが効率としては上なはず
    # the result will be
    # 0 --- 280
    # ||---
    # 100
    edges = [image.detect_line(img, i)[0] for i in (20, 180)]
    # edges[0] --> right,  edges[1] --> left
    # 条件がかなり緩いから本番環境でしきい値とらないといけない
    # たぶん値が小さい時　= 上の方にある時は無視するみたいな感じのコードでやっていくと良いんじゃないでしょうか
    # --> 結局しきい値を設定してやっそれ以下なら緑として認めないような仕組みを採用
    # 交差点かどうかの検出には遠くの方でまっすぐかどうかも条件に含めないとカーブをT字路判定してしまう
    threash = 400 # in 480
    right = edges[0] > threash
    left = edges[1] > threash
    if not (right or left):
        return "straight" # go straight
    elif left and right:
        return "cross"
    elif right:
        return "right"
    elif left:
        return "left"
