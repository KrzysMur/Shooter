import cv2 as cv
import numpy as np
import math
from datetime import datetime
from config import *


class Shot:
    def __init__(self, circle):
        self.timestamp = datetime.now()
        self.circle = [int(x) for x in circle]


    def get_dist(self):
        self.dist = int(math.sqrt((screen_center[0] - self.circle[0])**2 + (screen_center[1] - self.circle[1])**2))

    def calc_val(self):
        ppmm = self.circle[2]/26.5
        dist_abs = self.dist / ppmm
        dist_from_ex = cal_ex_target_diam - dist_abs
        if dist_abs <= cal_ten_x_diam/2:
            self.score = round(((cal_ten_x_diam/2 - dist_abs) / inner_tenth) / 10 + 10.4, 1)
        elif dist_abs <= cal_ten_diam/2:
            self.score = round(((cal_ten_diam/2 - dist_abs) / outer_tenth) / 10 + 10, 1)
        elif dist_abs <= cal_ex_target_diam/2:
            self.score = round((dist_from_ex / tenth + 10) / 10 - 10, 1)
        else:
            self.score = 0

    def print_shot_stats(self):
        print(f"Score: {self.score}, time: {self.timestamp}")


def vid_source_init(cam):
    print("Initializing the camera")
    try:
        global cap, screen_center, screen_dimentions
        cap = cv.VideoCapture(cam)
        ret, frame = cap.read()
        screen_center = [frame.shape[1] // 2, frame.shape[0] // 2]
        screen_dimentions = frame.shape
    except Exception:
        print("Can't initialize camera.")
    else:
        print("Camera initialized successfully")


def frame_process():
    ret, frame = cap.read()
    output = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return cv.blur(output, (blur, blur))
    
def search_circle(output, min, max):
    circle = cv.HoughCircles(output, cv.HOUGH_GRADIENT, 1, 20 ,param1=50, param2=30, minRadius=min, maxRadius=max)
    if circle is not None:
        return circle[0][0]

def draw_circle(circle, output):
    if circle is not None:
        cv.circle(output, (int(circle[0]), int(circle[1])), int(circle[2]), (255, 255, 255), 1)
    cv.circle(output, (screen_center[0], screen_center[1]), 2, (255, 255, 255), -1)

def shot_listener(circle):
    if cv.waitKey(1) == ord('s') and circle is not None:
        return True
    return False


