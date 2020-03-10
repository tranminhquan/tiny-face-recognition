import os
import shutil
dirname = os.path.dirname(__file__)
os.sys.path.append(dirname)
# os.sys.path.append('D:\\FR_demo_3\\server\\resources')
# os.sys.path.append('D:\\FR_demo_3\\server\\ai\\models\\cv')
os.sys.path.append(os.path.join(dirname, '../ai/models/cv'))
os.sys.path.append(os.path.join(dirname, '../'))

print(dirname)
print(os.path.join(dirname, '../ai/models/cv'))

from flask_restful import fields, marshal_with, reqparse, Resource
from flask import jsonify
import werkzeug
from werkzeug.utils import secure_filename
from ..utils.db_utils import *
from ..ai.models.cv.load_model import *
from bson.json_util import dumps
# import json
from skimage.io import imread, imsave



post_parser = reqparse.RequestParser()
post_parser.add_argument('images',
                            type=werkzeug.datastructures.FileStorage,
                            location='files',
                            required='True',
                            action='append')
post_parser.add_argument('r', type=float)
post_parser.add_argument('alpha', type=float)
post_parser.add_argument('beta', type=float)
post_parser.add_argument('gamma', type=float)
post_parser.add_argument('delta', type=float)
post_parser.add_argument('e_s', type=float)
post_parser.add_argument('e_b', type=float)
post_parser.add_argument('dataset_id', type=str)


class Prediction(Resource):

    def __init__(self):
        
        super()
        self.db = init_database()
    
    def get(self):
        # get all fomular and dataset info
        # all_f = self.db.dataset.find()

        # get all training info
        training = self.db.training.find()
        all_d = []
        all_f = []
        for t in training:
            # get all related dataset
            temp_data = self.db.dataset.find({'_id': t['dataset']})
            temp_f = self.db.fomular.find({'_id': t['fomular']})
            all_d.append(temp_data[0])
            all_f.append(temp_f[0])

        print('len all_d: ', len(all_d))
        print('len all_f: ', len(all_f))

        return {'dataset_info': dumps(all_d), 'fomular_info': dumps(all_f)}


    def post(self):
        'images, r, alpha, beta, gamma, delta, e_s, e_b, dataset_id'

        images = []

        #save temp image
        data = post_parser.parse_args()
        
        # acc = np.array([1., 2., 3.])
        # val_acc = np.array([4., 5., 6.])

        # response = {}
        # history = {}
        # history['acc'] = list(acc)
        # history['val_acc'] = list(val_acc)

        # response['training_info'] = history
        # return response

        image_urls = []
        image_names = []
        if data['images']:
            for index, img in enumerate(data['images']):
                mime = img.mimetype
                if mime == 'image/jpeg' or mime == 'image/png':
                    imname = secure_filename(img.filename)
                    image_names.append(imname)
                    # p = './predict_image_' + str(index) + '_' + str(imname)
                    p_upload = './static/predict_image_' + str(index) + '_' + str(imname)
                    image_urls.append('http://localhost:5000/static/' + 'predict_image_' + str(index) + '_' + str(imname))
                    # print(p)
                    img.save(p_upload)
                    # img.save(p_upload)
                    # shutil.move(p, p_upload)
        
        # load model and fomular
        ##  find path from training database where dataset= and fomular=
        ##  get r and alpha, beta, gamma, delta, e_s, e_b, ... (for prediction)

        
        for index, img in enumerate(data['images']):
            # load image
            imname = secure_filename(img.filename)
            image = imread('./static/predict_image_' + str(index) + '_' + str(imname))
            images.append(image)

        r = data['r']
        alpha = data['alpha']
        beta = data['beta']
        gamma = data['gamma']
        delta = data['delta']
        e_s = data['e_s']
        e_b = data['e_b']
        dataset_id = data['dataset_id']

        print(r,alpha,beta,gamma,delta,e_s,e_b,dataset_id)

        method_labels, method_accs, history, (M_s, N_s) = predict_fomular_model(images, r, alpha, beta, gamma, delta, e_s, e_b, dataset_id)
        other_labels, other_accs, interpolate_images = predict_original_model(images, r, alpha, beta, gamma, delta, e_s, e_b, dataset_id)

        method_accs = np.around(method_accs, 4)
        other_accs = np.around(other_accs, 4)
        print(interpolate_images.shape)
        print(interpolate_images)
        interpolate_image_urls = []

        for i in range(len(data['images'])):
            nb_p = './static/nb_' + image_names[i]
            bilinear_p = './static/bilinear_' + image_names[i]
            bicubic_p = './static/bicubic_' + image_names[i]

            imsave(nb_p, interpolate_images[3*i+0])
            imsave(bilinear_p, interpolate_images[3*i+1])
            imsave(bicubic_p, interpolate_images[3*i+2])

            interpolate_image_urls.append('http://localhost:5000/static/' + 'nb_' + image_names[i])
            interpolate_image_urls.append('http://localhost:5000/static/' + 'bilinear_' + image_names[i])
            interpolate_image_urls.append('http://localhost:5000/static/' + 'bicubic_' + image_names[i])

        print('Fomular-------------')
        print(method_labels, method_accs)
        print(history)

        print('Original------------')
        print(other_labels, other_accs)

        # normalize history
        history['acc'] = list(history['acc'])
        history['val_acc'] = list(history['val_acc'])
        history['loss'] = list(history['loss'])
        history['val_loss'] = list(history['val_loss'])

        # parse response
        response = {}
        response['training_info'] = history
        predictions = []
        for i in range(len(data['images'])):
            predictions.append(
                {
                    'method': 
                    {
                        'label': method_labels.tolist()[i],
                        'accuracy': round(method_accs.tolist()[i],4),
                    }, 
                    'nb': 
                    {
                        'label': other_labels.tolist()[i*3],
                        'accuracy': other_accs.tolist()[i*3],
                    },
                    'bilinear': 
                    {
                        'label': other_labels.tolist()[i*3+1],
                        'accuracy': other_accs.tolist()[i*3+1],
                    },
                    'bicubic': 
                    {
                        'label': other_labels.tolist()[i*3+2],
                        'accuracy': other_accs.tolist()[i*3+2],
                    }
                })
            
        response['predictions'] = predictions
        response['image_urls'] = image_urls
        response['interpolate_image_urls'] = interpolate_image_urls
        response['model_size'] = str(M_s) + ' x ' + str(N_s)
        response['image_size'] = str(images[0].shape[0]) + ' x ' + str(images[0].shape[1])
        print(response)

        return response


        # return {'message': 'ok'}
        # return {
        #     'training_info': 
        #         {
        #             'epochs': ,
        #             'acc': ,
        #             'val_acc': ,
        #             'loss': ,
        #             'val_loss': ,
        #         },
        #     'predictions':
        #         [{
        #             'method': 
        #             {
        #                 'label':, ,
        #                 'accuracy': ,
        #             },
        #             'nb': 
        #             {
        #                 'label':, ,
        #                 'accuracy': ,
        #             },
        #             'bilinear': 
        #             {
        #                 'label':, ,
        #                 'accuracy': ,
        #             },
        #             'bicubic': 
        #             {
        #                 'label':, ,
        #                 'accuracy': ,
        #             }
        #         }]
        #     }

            


