import cv2 as cv
import numpy as np
import math
from datetime import datetime
from config import *


class Shot:
    def __init__(self, circle):
        self.timestamp = datetime.now()
        self.shot_num = None
        self.circle = [int(x) for x in circle]
        self.inner_flag = ""
        self.score = None
        self.no_decimal_score = None

    def get_dist(self):
        self.dist = int(math.sqrt((screen_center[0] - self.circle[0])**2 + (screen_center[1] - self.circle[1])**2))

    def calc_val(self):
        ppmm = self.circle[2]/26.5
        dist_abs = self.dist / ppmm
        dist_from_ex = cal_ex_target_diam - dist_abs
        if dist_abs <= cal_ten_x_diam/2:
            self.inner_flag = "X"
            self.no_decimal_score = 10
            self.score = round(((cal_ten_x_diam/2 - dist_abs) / inner_tenth) / 10 + 10.4, 1)
        elif dist_abs <= cal_ten_diam/2:
            self.no_decimal_score = 10
            self.score = round(((cal_ten_diam/2 - dist_abs) / outer_tenth) / 10 + 10, 1)
        elif dist_abs <= cal_ex_target_diam/2:
            self.score = round((dist_from_ex / tenth + 10) / 10 - 10, 1)
            self.no_decimal_score = int((dist_from_ex / tenth + 10) / 10 - 10)
        else:
            self.score = 0
        self.score = round(self.score, 1)

    def print_shot_stats(self):
        print(f"{self.shot_num}: {self.score}{self.inner_flag}, time: {self.timestamp}")


class Session:
    def __init__(self, num_of_shots):
        self.num_of_shots = num_of_shots
        self.num_of_inners = 0
        self.score = 0
        self.no_decimal_score = 0

    def new_shot(self, circle, shot_num):
        shot = Shot(circle)
        shot.shot_num = shot_num
        shot.get_dist()
        shot.calc_val()
        shot.print_shot_stats()
        self.score += shot.score
        self.score = round(self.score, 1)
        self.no_decimal_score += shot.no_decimal_score
        if shot.inner_flag == "X":
            self.num_of_inners += 1

    def session(self):
        shot_num = 1
        while shot_num <= self.num_of_shots:
            output = frame_process()
            circle = search_circle(output, min, max)
            if shot_listener(circle):
                self.new_shot(circle, shot_num)
                shot_num += 1
            draw_circle(circle, output)
            cv.imshow("Kamerka", output)
        cv.destroyAllWindows()

    def print_session_stats(self):
        print(f"""
        Stats of this session
            Number of shots: {self.num_of_shots}
            Total score: {self.score}
            Score without decimal: {self.no_decimal_score}
            Number of inner tens: {self.num_of_inners}
            Average shot: {round(self.score / self.num_of_shots, 1)}
              """)


class Command:
    def __init__(self, command):
        self.cmd = command
        self.cmd = self.cmd.split()

    def execute(self):
        try:
            match self.cmd[0]:
                case "s":
                    session = Session(int(self.cmd[1]))
                    session.session()
                    session.print_session_stats()
                case "help":
                    print("- 's 10' - s command starts a new session. The number represents the amount of shots in this session")
                case _:
                    print("Command doen't exist")
        except Exception as e:
            print("Can't execute this command", e)


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


