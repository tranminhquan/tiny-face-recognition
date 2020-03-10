from flask_pymongo import MongoClient
import numpy as np


def init_database():
    # # database
    # app.config['MONGO_URI'] = 'mongodb://localhost:27017/deeplearning'
    # mongo = PyMongo(app)
    # return mongo

    client = MongoClient('mongodb://localhost:27017/')
    db = client.deeplearning
    return db

def add_sample_data(mongo):
    f_id = mongo.fomular.insert({
        'r': 0.2,
        'alpha': 2.5,
        'beta': 0.5,
        'gamma': 1.0,
        'delta': 0.5,
        'e_s': 0,
        'e_b': 0
    })

    d_id = mongo.dataset.insert({
        'dataset_id': "ORL",
        'path': "orl",
        'n_data': 400,
        'labels': np.arange(40).tolist(),
        'data': [10 for k in np.arange(40)]
    })

    t_id = mongo.training.insert({
        'dataset': d_id,
        'fomular': f_id,
        'path': '0.2000_2.5000_0.5000_1.0000_0.5000_0.0000_0.0000_ORL'
    })


def createFomular(mongo, value):
    _id = mongo.db.fomular.insert(value)
    return _id

def createModel(mongo, value):
    pass

def createDataset(mongo, value):
    pass

def createTraining(mongo, value, datasetid):
    pass

# db = init_database()
# add_sample_data(db)
