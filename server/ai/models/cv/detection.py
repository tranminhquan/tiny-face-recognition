import os
dirname = os.path.dirname(__file__)
os.sys.path.append(dirname)
import numpy as np
import cv2

class FaceDetection():
    '''
    Face detection using Cascade from opencv
    '''
    def __init__(self, MAX_FRAMES=3):
        self.classifier = cv2.CascadeClassifier(os.path.join(dirname, './haarcascade_frontalface_default.xml'))
        self.max_frames = MAX_FRAMES
        self.colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (0,0,0)]

    def detect(self, frame):
        '''
        Detect face
        -------------
        frame: list or numpy array
        -------------
        Return
            frame with drawed bounding box
            list of cropped bounding box
        '''
        frame = np.asarray(frame, dtype=np.uint8)
        if np.max(frame) <= 1:
            frame = frame*255

        boxes = self.classifier.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

        cropped_images = []
        drawed_frame = frame

        for i in range(len(boxes)):
            if i >= self.max_frames:
                break
            cropped_images.append(frame[boxes[i][1]:boxes[i][1]+boxes[i][3], boxes[i][0]:boxes[i][0]+boxes[i][2]])
            drawed_frame = cv2.rectangle(drawed_frame, (boxes[i][0], boxes[i][1]), 
                            (boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3]), 
                            self.colors[i], 3)

        return drawed_frame, cropped_images
