import buildhat as bh
from time import sleep


class Motor:
    def __init__(self, left, right):
        self.tank = bh.MotorPair(left, right)

    def power_limit(self, power):
        return max(min(50, power),-50)

    def on(self, left, right):
        self.tank.start(self.power_limit(left), self.power_limit(-right))
    
    def off(self):
        self.tank.stop()
    
    def turn(self, deg):
        if deg < 0:
            self.tank.run_for_degrees(270*deg/90,10,10)
        else:
            self.tank.run_for_degrees(270*deg/90, -10,-10)

if __name__ == "__main__":
    tank = Motor("C", "D")
    tank.on(60, 30)
    sleep(10)
    tank.off()
