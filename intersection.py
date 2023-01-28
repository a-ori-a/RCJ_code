import cv2
import pandas as pd
import image

# how to detect intersection
# fot each (top, center, bottom), judge (left, center, right) and then integrate the answer
# switch by the combined chars

def around(standard, num, thresh=10):
    if abs(num - standard) < thresh:
        return True
    else:
        return False

def intersection(points: list):
    print(points)
    if -1 in points:
        return 'unstable'
    mean = (points[0] + points[2])/2
    if (not around(points[1], mean, 35)) and (points[1] == max(points) or points[1] == min(points)):
        return 't_road'
    else:
        return 'straight'



    result = ""
    for point in points:
        condition = around(100, point[0], 20)
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

def intersection_img(hsv):
    interlists = pd.Series([image.detect_line(hsv, y) for y in range(299, -1, -1)])
    top_btm = (interlists[0]+interlists[-1]) / 2
    mean = interlists.mean()
    if not around(top_btm,mean, 30):
        return 't_road'
    else:
        return 'straight'

def intersection_bad(img, line_position):
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # 画像を左向きに90°回転させてimage.pyで作ったdetect_lineを適応できるようにした
    # 関数を乱用してる感じはするけどこっちのほうが効率としては上なはず
    # the result will be
    # 0 --- 280
    # ||---
    # 100
    if line_position < 40 or line_position > 159:
        edges = [0, 0]
    else:
        edges = [image.detect_line(img, i)[0] for i in (line_position-10, line_position+10)]
    # edges[0] --> right,  edges[1] --> left
    # 条件がかなり緩いから本番環境でしきい値とらないといけない
    # たぶん値が小さい時　= 上の方にある時は無視するみたいな感じのコードでやっていくと良いんじゃないでしょうか
    # --> 結局しきい値を設定してやっそれ以下なら緑として認めないような仕組みを採用
    # 交差点かどうかの検出には遠くの方でまっすぐかどうかも条件に含めないとカーブをT字路判定してしまう
    threash = 440 # in 480
    right = edges[0] > threash
    left = edges[1] > threash
    if (right and not left) or (not right and left):
        return 't_road'
    else:
        return 'straight'