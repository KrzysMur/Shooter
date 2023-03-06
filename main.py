from shooter import *

def main():
    vid_source_init(cam_n)
    while True:
        try:
            command = Command(input(">>> "))
            command.execute()
        except Exception:
            print("High level exception occured")


if __name__ == "__main__":
    main()