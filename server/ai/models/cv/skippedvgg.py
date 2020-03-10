from models.cv.basemodel import BaseModel, BaseModelBuilder
from keras.models import *
from keras.callbacks import *
from keras.layers import *
from keras.layers.core import *
from keras import backend as K
from keras.optimizers import *
from keras.losses import *
import os
import numpy as np
import matplotlib.pyplot as plt
import keras


class SkippedVGGBuilder(BaseModelBuilder):
    def __init__(self, **kwargs):
        super(SkippedVGGBuilder, self).__init__(**kwargs)

    def build(self, nb_blocks, input_shape, num_classes, nb_layers, nb_neurons, include_top=True, verbose=1, **kwargs):
        '''
        Build Skipped VGG model
        ----------------------------------
        nb_blocks: number of block in model
        input_shape: tuple, size of 3, not include batch size
        num_classes: number of model output
        nb_layers:  list, nb of conv layer in each block; 
                    if scalar, then all blocks are used the same number of conv layer
        nb_neurons: list, nb of conv neuron in each block
        include_top: wheather the model include classifier or not
        -----------------------------------
        Return: Keras model
        '''

        concats = []
        for i in range(nb_blocks):
            concats.append([])

        if type(nb_layers) is int:
            temp = nb_layers
            nb_layers = []
            for i in range(nb_blocks):
                nb_layers.append(temp)

        if verbose:
            print('Create DensedVGG model with ' + str(nb_blocks) +
                  ' blocks, input shape = ' + str(input_shape))

        for i in range(nb_blocks):
            if verbose:
                print('Create block ' + str(i) + ':')

            if i == 0:  # First block
                b = Input(shape=input_shape)
                inputs = b

            # check all layers before
            if len(concats[i-1]) > 1:
                if verbose:
                    print('Concatenate ', concats[i-1])
                b = concatenate(concats[i-1])
            elif len(concats[i-1]) == 1:
                if verbose:
                    print('Get direct output from the previous block ',
                          concats[i-1])
                b = concats[i-1][0]

            # create main block
            b = self._define_block(b, nb_layers[i], nb_neurons[i], index=i)
            concats[i].append(b)

            # create cropping layer
            for j in range(i+1, nb_blocks):
                if verbose:
                    print('-- create skipped connection from block ' +
                          str(i) + ' to block ' + str(j+1) + ' ...')

                src_shape = b.get_shape()
                src_shape = (int(src_shape[1]), int(
                    src_shape[2]), int(src_shape[3]))
                dst_shape = (src_shape[0]//2**(j-i),
                             src_shape[1]//2**(j-i), src_shape[2])

                print(src_shape, dst_shape)
                h = src_shape[0] - dst_shape[0]
                w = src_shape[1] - dst_shape[1]
                if h % 2 == 0:
                    h_0 = h // 2
                    h_1 = h // 2
                else:
                    h_0 = h // 2
                    h_1 = (h // 2) + 1

                if w % 2 == 0:
                    w_0 = w // 2
                    w_1 = w // 2
                else:
                    w_0 = w // 2
                    w_1 = (w // 2) + 1

                concat_layer = Cropping2D(
                    ((h_0, h_1), (w_0, w_1)), name='cropping_block' + str(i) + '_block' + str(j+1))(b)
                concats[j].append(concat_layer)

        # top model
        if verbose:
            print('Create top model')

        if len(concats[nb_blocks-1]) == 1:
            outputs = concats[nb_blocks-1]
        else:
            outputs = concatenate(concats[nb_blocks-1])

        outputs = GlobalAveragePooling2D()(outputs)
        outputs = Dense(num_classes)(outputs)
        outputs = BatchNormalization()(outputs)
        outputs = Activation('softmax')(outputs)

        self.model = Model(inputs=inputs, outputs=outputs)

        # compileext install k--kato.docomment
        self.model.compile(loss=categorical_crossentropy,
                           optimizer=Adam(), metrics=['accuracy'])

        if verbose:
            self.model.summary()
        return self.model

    def _define_block(self, input_layer, nb_layers, nb_neurons, kernel_size=(3, 3), batch_normalization=True, activation='relu', **kwargs):
        index = None
        if 'index' in kwargs:
            index = kwargs['index']

        for i in range(nb_layers):
            if i == 0:
                b = input_layer

            b = Conv2D(nb_neurons, kernel_size=kernel_size, strides=1,
                       padding='same', name='conv' + str(i) + '_block' + str(index))(b)
            if batch_normalization:
                b = BatchNormalization(
                    name='batchnorm' + str(i) + '_block' + str(index))(b)
            b = Activation(activation, name=activation +
                           str(i) + '_block' + str(index))(b)
        b = MaxPooling2D(pool_size=(
            2, 2), name='maxpooling_block' + str(index))(b)
        return b


def SkippedVGG3Blocks(include_top=True, weights=None, input_shape=None,
                      batch_normalization=True, classes=None, verbose=0):
    return SkippedVGGBuilder().build(3, input_shape=input_shape, num_classes=classes,
                                     nb_layers=[2, 2, 3], nb_neurons=[64, 128, 256], verbose=verbose)
