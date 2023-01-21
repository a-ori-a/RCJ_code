import buildhat as bh
from time import sleep


class Motor:
    def __init__(self, left, right):
        self.tank = bh.MotorPair(left, right)

    def on(self, left, right):
        self.tank.start(left, -right)
    
    def off(self):
        self.tank.stop()

tank = Motor("C", "D")
tank.on(100, 100)
sleep(10)
tank.off()