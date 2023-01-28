import cv2
import pandas as pd
import subprocess

# imageの配列のイメージ  ←?
"""
[ クソデカ大かっこ

	[   なんとも言えないカッコ
		(
			それぞれのピクセルのやつ
		)
	]
]

覚えておきましょう
H S V
↓ ↓ ↓ 
B G R
"""

def hsv(img): # convert image from bgr to hsv
	img = cv2.blur(img, (5,5)) # 画像にぼかしをかける
	img = cv2.resize(img, (200, 480)) # ぼかした画像をさらに縮小してい感じにする
	return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def is_color(img,x,y):
	pixel = img[y][x]
	print(pixel)
	if 60 < pixel[0] < 90 and 150 < pixel[1] and 20 < pixel[2]:
		return 'green'
	elif pixel[2] < 40:
		return 'black'
	else:
		return 'white'

def detect_line_2a(img):
	cv2.imwrite('./photo.jpg', img)
	btm = subprocess.run(['jp2a', './photo.jpg'],capture_output=True, text=True).stdout.split('\n')[-2]
	btm_length = len(btm)
	blacks = []
	for i,pixel in enumerate(btm):
		if pixel == ' ':
			blacks.append(i)
	return sum(blacks)/(len(blacks)+1)/btm_length


def detect_line(img, ypos=300): # the image needs to be hsv
	# returns the center of the detected line of ypos in a (x, y) format
	data = [x[2] for x in img[ypos]]
	line_list = pd.Series([x for x,y in enumerate(data) if y < 40])
	if len(line_list) == 0:
		mean = -1
	else:
		mean = line_list.mean()
	mean = int(mean)
	display.line_indicator(mean)
	return (mean, ypos)

def turn_strength(img, ypos): # set y-position of top and btm
	power = detect_line(img, ypos)[0]
	if power == -1:
		print('no line found')
		return [0,-1]
	else:
		return [power - 100, power]
	

def draw(img, follows:list, intersections:list):
	# No need to run in CLI mode
	# just for debugging (+eye candy?)
	#     120 ~ 520
	# 200
	#  ↓
	# 350
	cv2.rectangle(img, (120, 200), (520, 350), (12, 200, 56), thickness=2)
	cv2.rectangle(img, (180, 380), (460, 475), (50, 100, 255), thickness=2)
	for i in follows:
		cv2.circle(img, i, 5, (255, 242, 0), thickness=-1)
	
	for i in intersections:
		cv2.circle(img, i, 5, (255, 242, 0), thickness=-1)

# ------
# Don't use the functions below
# They are outdated
# ------

def gray(img):
	ret, result = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_OTSU)
	return result

def detect_line_grayscale(image, ypos, result):
	data = image[ypos]
	blacklist = pd.Series([x for x,y in enumerate(data) if y==0])
	while image[ypos][int(blacklist.mean())] != 0 and len(blacklist) > 10:
		blacklist = blacklist[blacklist.quantile(0.1)<blacklist][blacklist<blacklist.quantile(0.9)] 
	try:
		# these cause bugs when no black color is detected
		mean = int(blacklist.mean())
		std = 2*int(blacklist.std())
	except:
		# so set them to 0 for now
		mean = 0
		std = 0
	if type(result) != bool:
		try:
			cv2.circle(result, (mean, ypos), 8, (0,0,255), thickness=-1)
			cv2.circle(result, (mean-std, ypos), 8, (0,255,0), thickness=-1)
			cv2.circle(result, (mean+std, ypos), 8, (0,255,0), thickness=-1)
		except:
			pass
	return (mean)

def simple(img, ypos, result=False):
	data = pd.Series(img[ypos])
	left_side = 0
	right_side = 0
	if 0 in data:
		check_counter = 0
		while data[check_counter] == 255:
			check_counter += 1
		left_side = check_counter
		while data[check_counter] == 0 and check_counter < 639:
			check_counter += 1
		right_side = check_counter
	cv2.circle(img, (left_side, ypos), 10, (255,255,255), thickness=-1)
	cv2.circle(img, (right_side, ypos), 10, (255,255,255), thickness=-1)
	return int((left_side+right_side)/2)


if __name__ == '__main__':
	cap = cv2.VideoCapture(0)
	while True:
		ret, frame = cap.read()
		frame = hsv(frame)
		print(turn_strength(frame,300))
