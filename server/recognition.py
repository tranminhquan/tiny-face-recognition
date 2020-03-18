import cv2
import numpy as np
import argparse
from ai.models.cv.detection import FaceDetection
from ai.models.cv.recognition import FaceRecognition
from ai.utils.visualization import stack_images

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--path', help='path to load video')
parser.add_argument('-s', '--save', help='path to save video')

args = parser.parse_args()

cap = cv2.VideoCapture(args.path)

detector = FaceDetection(MAX_FRAMES=1)
predictor = FaceRecognition(None, './demo_label_dict.hdf5')

out = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc('M','J','P','G'), 15, (int(cap.get(3)), int(cap.get(4))))

colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (0,0,0)]

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0,255,0)
line_type = 2

while (cap.isOpened()):
    ret, frame = cam.read()
    cams = []

    if ret is False:
        break

    tframe, cropped_frames = detector.detect(frame)

    if cropped_frames is not None:
        for i,fr in enumerate(cropped_frames):
            # _, self.label, self.prob = self.predictor.predict(fr, None)
            _, label, prob, cam = predictor.predict_with_heatmap(fr, None)
            cams.append(cam)
            cv2.putText(tframe, str(label) + ': ' + str(prob), (10 + 400*i,30), font, font_scale, colors[i], line_type)

        out_frame = stack_images(tframe, cropped_frames, cams)
        out_frame = np.asarray(out_frame*255, dtype=np.uint8)
        out.write(out_frame)

    else:
        out.write(frame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()


