class Green:
    def __init__(self):
        self.ypos = 200
        self.fail_counter = 0

    def has_green(self, img):
        data = img[self.ypos]
        data = [ x for x,y in enumerate(data) if 60 < y[0] < 90 and 150 < y[1] and 20 < y[2]]
        if len(data) < 5: data = []  #データに含まれている緑の点の個数が5個より少なかったらデータを初期化する
        return data
    
    def catch_green(self, img, line_x):
        if self.fail_counter >= 5:
            self.fail_counter = 0
            self.ypos = 200
            return
        green_found = has_green(img)
        if green_found: # 緑発見
            self.fail_counter = 0
            if self.ypos > 280: # intersection.py で使われているthreshの値かそれより少し小さいぐらいが望ましい
                if line_state not in ["straight", "white"]: # 交差点が検出されていたら
                    left_green = 0
                    right_green = 0
                    for i in green_found:
                        if i < line_x:
                            left_green += 1
                        elif i > line_x:
                            right_green += 1
                    if left_green >= 5:
                        left_green = True
                    else:
                        left_green = False
                    if right_green >= 5:
                        right_green = True
                    else:
                        right_green = False
                    if line_state == "right" and left_green:
                        print("ERROR:green must not exist on left now.")
                        return "no"
                    elif line_state == "left" and right_green:
                        print("ERROR:green must not exist on right now.")
                        return "no"
                    else:
                        if right_green:
                            if left_green:
                                return "back"
                            else:
                                return "right"
                        elif left_green:
                            return "left"
                    self.ypos = 200 # reset the pointer
                else:
                    self.ypos -= 30
            else:
                self.fail_counter += 1
                self.ypos -= 30
        else:
            return "no"
        # 緑が見つからなかった時の処理は別に書かなくても大丈夫なはず...よね？