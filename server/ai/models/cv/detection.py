import os
dirname = os.path.dirname(__file__)
os.sys.path.append(dirname)
import numpy as np
import cv2

class FaceDetection():
    '''
    Face detection using Cascade from opencv
    '''
    def __init__(self):
        self.classifier = cv2.CascadeClassifier(os.path.join(dirname, './haarcascade_frontalface_default.xml'))

    def detect(self, frame):
        '''
        Detect face
        -------------
        frame: list or numpy array
        -------------
        Return
            frame with drawed bounding box
            cropped bounding box
        '''
        frame = np.asarray(frame, dtype=np.uint8)
        if np.max(frame) <= 1:
            frame = frame*255

        boxes = self.classifier.detectMultiScale(frame)
        if len(boxes) == 0:
            return None, None

        return cv2.rectangle(frame, (boxes[0][0], boxes[0][1]), 
                            (boxes[0][0] + boxes[0][2], boxes[0][1] + boxes[0][3]), 
                            (255,0,0), 3), frame[boxes[0][1]:boxes[0][1]+boxes[0][3], boxes[0][0]:boxes[0][0]+boxes[0][2]]
