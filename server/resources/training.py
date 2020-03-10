import os
os.sys.path.append('D:\\FR_demo_3\\server\\resources')

from flask_restful import fields, marshal_with, reqparse, Resource
from ..utils.db_utils import *
from bson.json_util import dumps

get_parser = reqparse.RequestParser()
get_parser.add_argument('dataset_id', type=str)

class Training(Resource):

    def __init__(self):     
        super()
        self.db = init_database()

    def get(self):
        data = get_parser.parse_args()

        dataset_id = str(data['dataset_id'])
        print(dataset_id)

        # get object id of dataset id
        dataset_info = self.db.dataset.find_one({'dataset_id': dataset_id})
        print(dataset_info)

        # get training info
        training_info = self.db.training.find_one({'dataset': dataset_info['_id']})
        print(training_info)

        # get corresponding fomular
        fomular_info = self.db.fomular.find_one({'_id': training_info['fomular']})
        print(fomular_info)

        response = {}
        response['dataset_info'] = dataset_info
        response['training_info'] = training_info
        response['fomular_info'] = fomular_info
        
        return dumps(response)