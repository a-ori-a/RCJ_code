import cv2
import numpy as np

def search_ball(hsv):
    low = np.array([0, 0, 0])
    high = np.array([255, 30, 150]) # 要調整
    img = cv2.inRange(hsv, low, high)