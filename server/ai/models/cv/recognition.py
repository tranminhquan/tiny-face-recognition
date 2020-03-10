import os

from keras.models import *
from keras.layers import *
import keras.backend as K
import cv2
import numpy as np
from skimage.transform import resize
import pickle
import tensorflow as tf

global graph
graph = tf.get_default_graph()

class FaceRecognition():
    '''
    Face recognition class
    ----------
    model_path: [str], path to saved model
    label_dict_path: str, path to label dictonary file (mapping between number and text label)
    '''
    def __init__(self, model_paths, label_dict_path):
        with graph.as_default():
            self.models = [load_model(os.path.join(os.path.dirname(__file__), path)) for path in model_paths]
            K.set_learning_phase(0)

            with open(os.path.join(os.path.dirname(__file__), label_dict_path), 'rb') as dt:
                self.label_dict = pickle.load(dt)


    def predict(self, image, model_index=0):
        '''
        predict label of image based on index of loaded model
        ----------------------
        Return:
            num_label: int
            str_label: text label
            prob: probability
        '''

        with graph.as_default():
            # resize to fit the input
            if self.models[model_index].input_shape[3] == 1:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            image = np.asarray(image, dtype='float')
            # print(image)
            image /= 255.

            image = resize(image, (self.models[model_index].input_shape[1], 
                                    self.models[model_index].input_shape[2], 
                                    self.models[model_index].input_shape[3]))

            image = np.expand_dims(image, axis=0)
            
            preds = self.models[model_index].predict(image, verbose=1)

            num_label = np.argmax(preds, axis=1)
            prob = np.max(preds, axis=1)
            print(num_label)
            try:
                str_label = self.label_dict[str(num_label[0])]
            except:
                str_label = None

            print(str_label)

            return num_label, str_label, prob
        



    