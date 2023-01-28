import image

class Green:
    def __init__(self):
        self.ypos = 200
        self.fail_counter = 0

    def has_green(self, img, line_y):
        data = img[line_y]
        data = [ x for x,y in enumerate(data) if 60 < y[0] < 90 and 150 < y[1] and 20 < y[2]]
        if len(data) < 5: data = []  #データに含まれている緑の点の個数が5個より少なかったらデータを初期化する
        return data
    
    def check_green(self, img, line_x, line_y):
        green_y = line_y
        black_count = 0
        white_count = 0
        flag = True
        while True:
            if green_y < 0:
                break
            color = image.is_color(img, line_x, green_y)
            if color == "white":
                white_count += 1
                black_count = 0
                if white_count >= 5:
                    break
            elif color == "black":
                black_count += 1
                white_count = 0
                if black_count >= 5:
                    flag = False
                    break
            else:
                black_count = 0
                white_count = 0
            green_y -= 1
        return flag
    
    def catch_green(self, img, line_x, line_y):
        green_found = self.has_green(img, line_y)
        if green_found: # 緑発見
            self.fail_counter = 0
            left_green = 0
            left_green_x = 0
            right_green = 0
            right_green_x = 0
            for i in green_found:
                if i < line_x:
                    left_green += 1
                    left_green_x += i
                elif i > line_x:
                    right_green += 1
                    right_green_x += i
            if left_green != 0:
                left_green_x = left_green_x / left_green
            if right_green != 0:
                right_green_x = right_green_x / right_green
            if left_green >= 5:
                left_green = True
            else:
                left_green = False
            if right_green >= 5:
                right_green = True
            else:
                right_green = False
            if left_green:
                left_green = self.check_green(img, left_green_x, line_y)
            if right_green:
                right_green = self.check_green(img, left_green_x, line_y)
            if right_green:
                if left_green:
                    return "back"
                else:
                    return "right"
            elif left_green:
                return "left"
        else:
            return "no"
        # 緑が見つからなかった時の処理は別に書かなくても大丈夫なはず...よね？