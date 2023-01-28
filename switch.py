import pigpio
from time import sleep

pi = pigpio.pi()

pi.set_mode(17, pigpio.INPUT)
while True:
    print(pi.read(17))
    # sleep(0.01)