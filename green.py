class Green:
    def __init__(self):
        self.ypos = 200
        self.fail_counter = 0

    def has_green(self, img, ypos):
        data = img[ypos]
        data = [ x for x,y in enumerate(data) if 60 < y[0] < 90 and 150 < y[1] and 20 < y[2]]
        if len(data) < 5: data = []  #データに含まれている緑の点の個数が5個より少なかったらデータを初期化する
        return data
    
    def catch_green(self):
        if self.fail_counter >= 5:
            self.fail_counter = 0
            self.ypos = 200
            return