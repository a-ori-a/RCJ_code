import cv2
from time import sleep
from green import Green
import image
import intersection
import motors
from lcd import LCD
from buildhat import DistanceSensor, Motor
import pigpio

# resolution 640x480
# 1  ~~~  640
# ...
# 480
# to
# 1  ~~~  100
# ...
# 480
pi = pigpio.pi()
pi.set_mode(17,pigpio.INPUT)
pi.set_mode(27,pigpio.INPUT)
cap = cv2.VideoCapture(0)
tank = motors.Motor("C", "D")
# catch = Motor('A')
# ds = DistanceSensor('B')
# ds.on()
# ds.get_distance()
try:
	display = LCD()
except:
	print('no lcd found')
green = Green()
default_speed = 11

if not cap.isOpened():
	print("No camera found")
	display.show('no camra')
	exit()

#-------------<<This is main>>----------------
d = 30
i = 0
t_road = 'pass'
counter = 0


def follow(img,ypos,scan=False,gain=1):
	global i,d, hsv
	if scan:
		_, frame = cap.read()
		img = image.hsv(frame)
	tmp, second = image.turn_strength(img, ypos)
	if second == -1:
		follow(img,0, scan=True, gain=0.7)
		return
	d = tmp - d
	power = ( tmp * 1 + d * 2 + i * 0 ) * gain
	d = tmp
	# i += tmp
	# print(power)
	tank.on(default_speed-power, default_speed+power)

# 1 → right
# -1 → left
which_to_turn = 1

# while True:
# 	ret, frame = cap.read()
# 	hsv = image.hsv(frame)
# 	follow(hsv, 460)


while True:
	display.show('hit the switch')
	follow([],480,scan=True)
	tank.off()
	while not pi.read(17):
		sleep(0.3)
	display.show('program start')
	sleep(0.5)
	while not pi.read(17):
		# いろいろ初期化
		counter += 1
		intersection_points = [340,400,460]
		ret, frame = cap.read()
		hsv = image.hsv(frame)
		line_x = image.detect_line(hsv,350)[0]
		print(line_x)

		if pi.read(27):
			tank.turn(-180)

		# 緑検出(優先度高)
		green_state = green.catch_green(hsv, line_x,350)
		if green_state != 'no': # 緑があったら
			tank.off() # 休憩
			display.show(green_state) # 最初の画面更新
			sleep(1)
			for i in range(10): # ちょっと進む
				follow(hsv, 460,scan=True,gain=0.4)
				sleep(0.05)
			tank.off() # 休憩
			_, frame = cap.read() # 写真撮影
			hsv = image.hsv(frame)
			tmp=green.catch_green(hsv, line_x,350)
			green_state = tmp if tmp != 'no' else green_state # 再検出
			display.show(green_state) # 再検出の画面更新
			sleep(1)
			if green_state == 'right':
				turn = 90
			elif green_state == 'left':
				turn = -90
			elif green_state == 'back':
				turn = 180
			elif green_state == 'no':
				turn = 90
			if green_state != 'no' and green_state != 'back':
				tank.off()
				sleep(1)
				for i in range(17):
					follow(hsv, 250, scan=True,gain=0.2)
					sleep(0.08)
			if green_state != 'no':
				tank.turn(turn)
				tank.off()
				display.show('turn finished')
		else:
			display.show(green_state)
		
		if (t_road := intersection.intersection(hsv, intersection_points)) != 't_road':
			follow(hsv, 460)
		elif t_road == 't_road':
			d = 0
			tank.off()
			display.show('intersection')
			sleep(0.3)
			for i in range(21):
				follow(hsv, 380, scan=True, gain=0.15)
				sleep(0.05)
			# exit()
		else:
			print(t_road)
		# display.show(t_road)
	display.show('program stopped')
	tank.off()
	sleep(2)