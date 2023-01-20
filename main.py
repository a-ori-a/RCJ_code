import cv2
from time import sleep
from concurrent.futures import ProcessPoolExecutor
from green import Green
import image
import intersection
import motors
from lcd import LCD

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
green = Green()

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
	# points = [image.detect_line(hsv, x) for x in [200, 275, 350]]
	# cross = intersection.intersection(points)
	if (line_state := intersection.intersection(hsv)) == 'straight':
		tank.on(50+power, 50-power)
	elif line_state == 'right':
		pass # turn right by 90 degree
	elif line_state == 'left':
		pass # turn left by 90 degree
	elif line_state == 'white':
		pass # gap or out of line
	else:
		print("could not see anything ...") # error
	display.show(line_state, 0)
	
	# 線の場所を表示するのはデバッグ用なら良いけど
	# 本番環境でやると二重に線の検出をすることになるし
	# わざわざpowerの返り値を追加するのもめんどくさいのでやめた方がいいと思います
 	display.line_indicator(image.detect_line(hsv, 460)[0])