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
# 479
# to
# 1  ~~~  200
# ...
# 479

cap = cv2.VideoCapture(0)
tank = motors.Motor("C", "D")
# catch = Motor('A')
ds = DistanceSensor('B')
try:
	display = LCD()
except:
	print('no lcd found')
green = Green()
default_speed = 20

if not cap.isOpened():
	print("No camera found")
	display.show('no camra')
	exit()
"""
d = 0
while True:
	ret, frame = cap.read()
	hsv = image.hsv(frame)
	# position = image.turn_strength(frame)
	# power = position*1.5 + (d-position)*0.5
	power = image.turn_strength(frame)
	power = max(min(power,50),-50)
	# d = position
	print(power)
	tank.on(default_speed - power, default_speed + power)
	# tank.on(default_speed+power, default_speed-power)
# """

while True:
	ret, frame = cap.read()
	hsv = image.hsv(frame)
	line_n = image.detect_line(hsv, 479)[0]-100
	line_f = image.detect_line(hsv, 300)[0]-100
	line_e = image.detect_line(hsb, 0)[0]-100
	if line_n == -101:
		if line_f == -101:
			if line_e == -101:
				line_state = "none"
				# maybe rescue zone
			else:
				line_state = "pd_p"
				pd_line = line_e
				# long gap's middle (?)
		else:
			line_state = "pd_s"
			pd_line = line_f
			# gap's middle
	elif line_f == -101:
		if line_e == -101:
			line_state = "back"
			# gap....?
		else:
			line_state = "pd_s"
			pd_line = line_e
	elif line_n < -5:
		if line_f < -5:
			sa = line_f - line_n
			if sa < -5:
				line_state = "left"
				# before cose out
			elif sa < 5:
				line_state = "pd_p"
				pd_line = line_n
			else:
				line_state = "straight"
		elif line_f <5:
			line_state = "straight"
		else:
			line_state = "pd_p"
			pd_line = line_f
	elif line_n < 5:
		if line_f < -5:
			line_state = "left"
		elif line_f < 5:

			# ima koko
	green_state = green.catch_green(hsv)
	if line_state == 'straight':
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
	elif line_state == 'cross':
		if green_state == 'back':
			pass
	else:
		print("could not see anything ...") # error
	display.show(line_state, 0)
