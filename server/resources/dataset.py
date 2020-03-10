import os
import shutil
import werkzeug
from werkzeug.utils import secure_filename

dirname = os.path.dirname(__file__)
os.sys.path.append(dirname)
os.sys.path.append(os.path.join(dirname, '..'))

from flask_restful import fields, marshal_with, reqparse, Resource

post_parser = reqparse.RequestParser()
post_parser.add_argument('captured_images',
                            type=werkzeug.datastructures.FileStorage,
                            location='files',
                            required='True',
                            action='append')
post_parser.add_argument('label', type=str)

class Dataset(Resource):
    def __init__(self):
        super()

    def post(self):
        data = post_parser.parse_args()
        base64 = data['captured_images']
        print('label: ', data['label'])

        self.create_dataset(data['label'], base64)


    def create_dataset(self, label, base64):
        root_dir = './ai/dataset'
        data_path = os.path.join(root_dir, str(label).lower())
        if not os.path.exists(data_path):
            os.mkdir(os.path.join(root_dir, str(label).lower()))
            counter = 0
        else:
            files = os.listdir(data_path)
            counter = int(os.path.basename(files[-1].split('_')[-1].split('.')[0]))
            counter += 1
        
        for index, img in enumerate(base64):
            img.save(os.path.join(data_path, str(label).lower() + '_' + str(counter) + '.png'))
            counter += 1
            
        return str(label).lower()