import RGB1602

class LCD:
    def __init__(self):
        # カメラが見つからなくてもエラーを吐かないように変更
        try:
            self.display = RGB1602.RGB1602(16, 2)
            self.open = True
        except:
            self.open = False

    def cursor(self, row):
        if not self.open: return
        if row == 0:
            self.display.setCursor(0, 0)
        elif row == 1:
            self.display.setCursor(0, 1)

    def show(self, string:str, row=None):
        if not self.open: return
        if string == None: return
        if row is None:
            self.cursor(0) # 基本的に上側に色々表示するはずだからカーソルを上に持っていくべき
            self.display.printout(string.center(16))
        else:
            self.cursor(row)
            self.display.printout(string.center(16))
    
    def line_indicator(self, center, row=1):
        if not self.open: return
        # センターは検出下線の中心のx座標で、
        # 0~200までの値を取る可能性があるから
        # 200で割ってディスプレイに表示可能な16文字をかけておく
        if center == -1:
            string = "________________"
        else:
            percentage = int(center/200*16)
            string = ("_"*(percentage-1)+"ooo").ljust(16, "_")
        self.show(string, row=row)