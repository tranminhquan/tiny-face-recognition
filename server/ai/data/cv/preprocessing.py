'''All preprocessing'''

from abc import ABC
from skimage.transform import resize
from skimage.io import imread
import numpy as np

class BaseDataPreprocessing(ABC):
    '''Abstract class, BaseDataPreprocessing'''
    def __init__(self, **kwargs):
        '''init'''
        super(BaseDataPreprocessing, self).__init__(**kwargs)

    def load_image(self, **kwargs):
        pass

    def resize(self, **kwargs):
        pass

    def reshape(self, **kwargs):
        pass

    def normalize(self, **kwargs):
        pass

    def preprocess(self, **kwargs):
        pass

class ImageDataPreprocessing(BaseDataPreprocessing):
    def __init__(self, image_shape, **kwargs):
        super(ImageDataPreprocessing, self).__init__(**kwargs)
        self.image_shape = image_shape

    def set_load_image_method(self, load_func, *args, **kwargs):
        load_func(*args, **kwargs)

    def load_image(self, image_path, **kwargs):
        super(ImageDataPreprocessing, self).load_image(**kwargs)
        return imread(image_path)

    def resize(self, image, target_size, **kwargs):
        '''
        target_size: tuple of 2
        '''
        super(ImageDataPreprocessing, self).resize(**kwargs)
        return resize(image, target_size)

    def reshape(self, image, target_shape, **kwargs):
        '''
        target_shape: tuple of 3
        '''
        super(ImageDataPreprocessing, self).reshape(**kwargs)
        return np.reshape(image, target_shape)

    def normalize(self, image, **kwargs):
        super(ImageDataPreprocessing, self).normalize(**kwargs)
        image /= 255
        return image

    def preprocess(self, image, **kwargs):
        super(ImageDataPreprocessing, self).preprocess(**kwargs)
        temp_image = np.array(image)
        if np.max(temp_image) <= 1:
            return temp_image
        return self.normalize(image, **kwargs)


    

    