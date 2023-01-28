import cv2
import numpy as np

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
