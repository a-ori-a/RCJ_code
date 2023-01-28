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
default_speed = 15

if not cap.isOpened():
	print("No camera found")
	display.show('no camra')
	exit()

#-------------<<This is main>>----------------
d = 0
i = 0
t_road = 'pass'

def follow(img,ypos,scan=False,gain=1):
	global i,d, hsv
	if scan:
		_, frame = cap.read()
		img = image.hsv(frame)
	tmp, _ = image.turn_strength(img, ypos)
	d = tmp - d
	power = ( tmp * 1 + d * 1 + i * -0 ) * gain
	d = tmp
	i += tmp
	print(power)
	tank.on(default_speed-power, default_speed+power)

# 1 → right
# -1 → left
which_to_turn = 1

while True:
	# いろいろ初期化
	intersection_points = [300,380,460]
	ret, frame = cap.read()
	hsv = image.hsv(frame)
	line_x = image.detect_line(hsv,350)[0]
	# 緑検出(最優先)
	if (green_state := green.catch_green(hsv, line_x,380)) == 'right':
		turn = 90
	elif green_state == 'left':
		turn = -90
	elif green_state == 'back':
		turn = 180 * which_to_turn
	if green_state != 'no': print(green_state)
	if green_state != 'no':
		tank.off()
		sleep(1)
		for i in range(10):
			follow(hsv, 250, scan=True,gain=0.2)
			sleep(0.08)
		tank.turn(turn)
	
	if (t_road := intersection.intersection(hsv, intersection_points)) != 't_road':
		follow(hsv, 460)
	elif t_road == 't_road':
		d = 0
		tank.off()
		print('intersection')
		sleep(0.3)
		for i in range(20):
			follow(hsv, 370, scan=True, gain=0.2)
			sleep(0.05)
		# exit()
	else:
		print(t_road)
	display.show(t_road)