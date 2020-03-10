# import os
# from flask import send_from_directory
# from flask_restful import fields, marshal_with, reqparse, Resource
# from ..utils.db_utils import *
# from bson.json_util import dumps

# post_parser = reqparse.RequestParser()
# post_parser.add_argument('filename', type=str)

# os.sys.path.append(os.path.dirname(__file__))

# class Upload(Resource):
#     def __init__(self):
#         super()

#     def get(self, path):
#         return send_from_directory('./static', path)

#     def post(self, path):
#         return send_from_directory('./static', path)

