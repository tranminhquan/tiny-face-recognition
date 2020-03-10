'''All generators for computer vision task are implemented here'''

'''
Note: 
    The dataset should have a csv file 
    which contains at least image_path 
    and its label, respectively
'''

from abc import ABC
from keras.utils import Sequence
import numpy as np
import pandas as pd
class BaseDataGenerator(ABC):
    '''Abstract class, BaseDataGenertor'''

    def __init__(self, **kwargs):
        '''init'''
        super(BaseDataGenerator, self).__init__(**kwargs)


class ImageTrainGenerator(Sequence):
    def __init__(self, csv_filepath, num_classes, batch_size, preprocessor, shuffle=False):
        self.current_epoch = 0
        df = pd.read_csv(csv_filepath)
        self.list_IDs = df['image_path'].tolist()
        self.num_classes = num_classes
        self.batch_size = batch_size
        self.preprocessor = preprocessor
        self.shuffle = shuffle
        self.on_epoch_end()

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
            self.current_epoch += 1

    def get_label_per_image(self, identifier):
        pass

    def __data_generation(self, temp_list_IDs):
        pass

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        # Generate data
        # X, y = self.__data_generation(list_IDs_temp)
        return X, y
