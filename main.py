from shooter import *

def main():
    vid_source_init(cam_n)
    while True:
        output = frame_process()
        circle = search_circle(output, min, max)
        if shot_listener(circle):
            shot = Shot(circle)
            shot.get_dist()
            shot.calc_val()
            shot.print_shot_stats()
        #draw_circle(circle, output)
        cv.imshow("Kamerka", output)

if __name__ == "__main__":
    main()