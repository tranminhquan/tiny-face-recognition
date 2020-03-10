
from flask import Flask, Blueprint
from flask_restful import Api
from flask_pymongo import PyMongo
from .utils.db_utils import *

from .resources.prediction import Prediction
from .resources.training import Training
# from .resources.upload import Upload
from .resources.dataset import Dataset
from .resources.stream import Stream
from flask_cors import CORS

import cv2
from flask import Response
import io


import os
from flask_restful import fields, marshal_with, reqparse, Resource

dirname = os.path.dirname(__file__)
os.sys.path.append(dirname)

app = Flask(__name__, static_url_path='/static')
CORS(app)
api = Api(app)

mongo = init_database()
# add_sample_data(mongo)

class Upload(Resource):
    def __init__(self):
        super()

    def get(self, path):
        return send_from_directory('static', path)

    def post(self, path):
        return send_from_directory('static', path)

api.add_resource(Prediction, '/predict')
api.add_resource(Training, '/training')
api.add_resource(Upload, '/upload/<path>')
api.add_resource(Dataset, '/dataset')
api.add_resource(Stream, '/stream')

vc = cv2.VideoCapture(0)
def gen():
    """Video streaming generator function."""
    while True:
        read_return_code, frame = vc.read()
        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
)

if __name__=='__main__':
    app.run(host='0.0.0.0:5000', debug=True, threaded=True)