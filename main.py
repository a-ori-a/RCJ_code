import cv2
from time import sleep
from green import Green
import image
import intersection
import motors
from lcd import LCD
from buildhat import DistanceSensor, Motor

# resolution 640x480
# 1  ~~~  640
# ...
# 480
# to
# 1  ~~~  100
# ...
# 480

cap = cv2.VideoCapture(0)
tank = motors.Motor("C", "D")
catch = Motor('A')
ds = DistanceSensor('B')
try:
	display = LCD()
except:
	print('no lcd found')
green = Green()
default_speed = 10

if not cap.isOpened():
	print("No camera found")
	display.show('no camra')
	exit()

while True:
    ret, frame = cap.read()
    hsv = image.hsv(frame)
    power = image.turn_strength(hsv, 380, 460)
    print(power)
    tank.on(default_speed+power, default_speed-power)

while True:
	ret, frame = cap.read()
	hsv = image.hsv(frame)
	# 線の検出&曲がる強さの計算
	power = max(50, min(image.turn_strength(hsv, 380, 460), -100))
	# 緑の状態確認
	green_state = green.catch_green(hsv)
	if (line_state := intersection.intersection(hsv)) == 'straight':
		tank.on(50+power, 50-power)
	elif line_state == 'right':
		if green_state == "no":
			pass # go straight
		elif green_state == "right":
			pass # turn right by 90 degree 
	elif line_state == 'left':
		if green_state == "no":
			pass # go straight
		elif green_state == "left":
			pass # turn left by 90 degree
	elif line_state == 'white':
		pass # gap or out of line
	else:
		print("could not see anything ...") # error
	display.show(line_state, 0)