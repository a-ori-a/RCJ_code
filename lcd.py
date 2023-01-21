import RGB1602

class LCD:
    def __init__(self):
        self.display = RGB1602.RGB1602(16, 2)

    def cursor(self, row):
        if row == 0:
            self.display.setCursor(0, 0)
        elif row == 1:
            self.display.setCursor(0, 1)

    def show(self, string:str, row=None):
        if row is None:
            self.display.printout(string.center(16))
        else:
            self.cursor(row)
            self.display.printout(string.center(16))
    
    def line_indicator(self, center, row=1):
        percentage = int(center/100*16)
        string = ("_"*(percentage-1)+"ooo").ljust(16, "_")
        self.show(string, row=row)