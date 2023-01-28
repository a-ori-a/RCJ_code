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
# catch = Motor('A')
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

#-------------<<This is main>>----------------
d = 0
# while True:
# 	ret, frame = cap.read()
# 	hsv = image.hsv(frame)
# 	# position = image.turn_strength(frame)
# 	# power = position*1.5 + (d-position)*0.5
# 	power = image.turn_strength(hsv, 460) * 1 # 1.7
# 	# power = max(min(power,50),-50)
# 	# d = position
# 	# tank.on(default_speed - power, default_speed)
# 	tank.on(default_speed-power, default_speed+power)

while True:
	ret, frame = cap.read()
	hsv = image.hsv(frame)
	# position = image.turn_strength(frame)
	# power = position*1.5 + (d-position)*0.5
	power, line_n = image.turn_strength(hsv, 450)#  * 1 # 1.7
	power *= 0.8
	line_f = image.detect_line(hsv, 350)[0]
	line_e = image.detect_line(hsv, 0)[0]
	# power = max(min(power,50),-50)
	# d = position
	# tank.on(default_speed - power, default_speed)
	# 緑の状態確認
	green_state = green.catch_green(hsv, line_n, 470)
	if green_state == 'no':
		line_state = '!intersection'
		if line_e == -1:
			line_y = 350 # line_f
		else:
			if abs(line_n) < abs(line_f):
				line_y = 450 # line_n
			else:
				line_y = 350 # line_f
		power, _ = image.turn_strength(hsv, line_y)
		power *= 0.8
		tank.on(default_speed-power, default_speed+power)
	else:
		if (line_state := intersection.intersection(hsv, line_n)) == 'straight':
			tank.on(default_speed-power, default_speed+power)
			pass
		elif line_state == 'right':
			if green_state == "right":
				pass # turn right by 90 degree 
			else:
				pass # error
		elif line_state == 'left':
			if green_state == "left":
				pass # turn left by 90 degree
			else:
				pass # error
		elif line_state == 'white':
			pass # error
		elif line_state == 'cross':
			if green_state == 'back':
				pass
			elif green_state == 'right':
				pass
			elif green_state == 'left':
				pass
		else:
			print("could not see anything ...") # error
	display.show(line_state, 0)
	print(line_state)
