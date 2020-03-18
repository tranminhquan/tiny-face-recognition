import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--path', help='path to save video')


args = parser.parse_args()

cam = cv2.VideoCapture(0)
width = int(cam.get(3))
height = int(cam.get(4))

out = cv2.VideoWriter(args.path, cv2.VideoWriter_fourcc('M','J','P','G'), 15, (width,height))

while True:
    ret, frame = cam.read()

    if ret is False:
        break

    out.write(frame)

    cv2.imshow('from webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
out.release()

cv2.destroyAllWindows()
