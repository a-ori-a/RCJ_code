class Green:
    def __init__(self):
        self.ypos = 200
        self.fail_counter = 0

    def has_green(self, img):
        data = img[self.ypos]
        data = [ x for x,y in enumerate(data) if 60 < y[0] < 90 and 150 < y[1] and 20 < y[2]]
        if len(data) < 5: data = []  #データに含まれている緑の点の個数が5個より少なかったらデータを初期化する
        return data
    
    def catch_green(self, img):
        if self.fail_counter >= 5:
            self.fail_counter = 0
            self.ypos = 200
            return
        green_found = has_green(img)
        if green_found: # 緑発見
            self.fail_counter = 0
            if self.ypos > 280: # intersection.py で使われているthreshの値かそれより少し小さいぐらいが望ましい
                if line_state not in ["straight", "white"]: # 交差点が検出されていたら
                    if line_state == "right":
                        pass
                    elif line_state == "left":
                        pass
                    elif line_state == "cross":
                        pass
                    self.ypos = 200 # reset the pointer
                else:
                    self.ypos -= 30
            else:
                self.fail_counter += 1
                self.ypos -= 30
        else:
            return "no"
        # 緑が見つからなかった時の処理は別に書かなくても大丈夫なはず...よね？