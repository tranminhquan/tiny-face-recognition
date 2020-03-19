import io
import cv2, threading, queue
from ..models.cv.recognition import FaceRecognition
from ..models.cv.detection import FaceDetection
import numpy as np

class VideoCapture:
    def __init__(self, name, width=640, height=480):
        self.cap = cv2.VideoCapture(name)
        self.cap.set(3, int(width))
        self.cap.set(4, int(height))
        print('camera resolution: ', self.cap.get(3), self.cap.get(4))
        # self.detector = FaceDetection()
        # self.predictor = FaceRecognition(['demo_face_model.hdf5'], 'demo_label_dict.hdf5')
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while self.cap.isOpened:
            ret, frame = self.cap.read()
            # frame, cropped_frame = self.detector.detect(frame)

            # print(np.asarray(frame).shape)
            # print(np.asarray(cropped_frame).shape)

            # _, str_label, prob = self.predictor.predict(cropped_frame, 0)

            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            # bytes_data = io.BytesIO()
            # frame.save(bytes_data, format='JPEG')
            self.q.put(frame)

    def read(self):
        return self.q.get()
        

def stream(video_capture):
    while(True):
        frame = video_capture.read()
        yield frame
        

def stop_stream(video_capture):
    video_capture.release()
    cv2.destroyAllWindows()

#################################333    

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# stream()
