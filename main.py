import cv2
from time import sleep
from concurrent.futures import ProcessPoolExecutor
import image
import intersection
import motors
from lcd import lcd

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
display = lcd()

if not cap.isOpened():
	print("No camera found")
	exit()

while True:
	ret, frame = cap.read()
	hsv = image.hsv(frame)
	# calculate power
	power = max(50, min(image.turn_strength(hsv, 380, 460), -100))
	# with ProcessPoolExecutor() as exe:
	# 	exe.submit(lambda img: max(50, min(image.turn_strength(img, 380, 460), -100)), hsv)

	# intersection detection
	points = [image.detect_line(hsv, x) for x in [200, 275, 350]]
	cross = intersection.intersection(points)
	if (cross := intersection.intersection(points)) == 'straight':
		tank.on(50+power, 50-power)
	elif cross == 'right':
		pass # turn right by 90 degree
	elif cross == 'left':
		pass # turn left by 90 degree
	elif cross == 'white':
		pass # gap or out of line
	else:
		print("could not see anything ...") # error