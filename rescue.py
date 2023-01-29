import cv2
import numpy as np
import image
from time import sleep
import pigpio

pi = pigpio.pi()
pi.set_mode(27,pigpio.INPUT)

def search_ball(hsv):
    low = np.array([0, 0, 0])
    high = np.array([255, 30, 150]) # 要調整
    img = cv2.inRange(hsv, low, high)
    imgEdge, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    balls = []
    for n in contours:
        ball_x = 0
        ball_points = 0
        for m in n:
            ball_x += m[0][0]
            ball_points += 1
        balls += ball_x / ball_points
    return balls

def find_wall():
    return pi.read(27)

box = 1
face = 0

def explore_rescuezone(tank):
    search_box = True
    position = 50
    while True:
        tank.on(10,10)
        sleep(0.1)
        if(find_wall()):
            tank.turn(180)
            if search_box:
                if box == face:
                    tank.move(160)
                    tank.turn(180)
                    tank.on(100,100)
                    sleep(0.5)
                    tank.move(-180)
                    tank.turn(180)
                    break
            face += 1
            if face == 4:
                position -= 25
                face = 0
                if position < 10:
                    position = 10
                    search_box = True
            tank.move(position)
            tank.turn(90)
    while True:
        tank.on(10, 10)
        sleep(0.1)
        if image.detect_line(460)[0] != -1:
            tank.move(400)
            break
        if(find_wall()):
            tank.turn(90)