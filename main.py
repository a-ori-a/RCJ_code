import cv2
from time import sleep
from concurrent.futures import ProcessPoolExecutor
import image
import intersection
import calculation
import motors

# resolution 640x480
# 1  ~~~  640
# ...
# 480

cap = cv2.VideoCapture(0)
tank = Motors("C", "D")

if not cap.isOpened():
	print("No camera found")
	exit()

while True:
	ret, frame = cap.read()
	hsv = image.hsv(frame)
	# calculate power
	power = max(50, min(image.turn_strength(hsv, 380, 460), -100))
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
	

    # cv2.putText(frame, "turn_strength : "+str(calculation.turn_strength(top[0], bottom[0])), (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (12,255,0), thickness=2)
    # cv2.putText(frame, intersection.intersection(points), (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (12, 255, 0), thickness=2)

    # frame = cv2.addWeighted(frame, 0.6, hsv, 0.4, 0)
    # image.draw(frame, [top, bottom], points)
    # cv2.imshow("hsv", hsv)
    # cv2.imshow("display", frame)
    #key = cv2.waitKey(30)
    #if key == 113:
    #    break
    #elif key == 115: # press S
    #    cv2.imwrite("./photo.jpg", frame)
