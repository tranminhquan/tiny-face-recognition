
from abc import ABC
from utils.thread_utils import TrainingThread

class BaseModel(ABC):
    '''Base model, most of functions use Keras API'''
    def __init__(self, **kwargs):
        '''init'''
        super(BaseModel,self).__init__(**kwargs)

    def compile(self, loss, optimizer, metrics):
        '''compile model'''

        pass

    def fit_generator(self, generator, batch_size, epochs, validation_generator=None, callbacks=None, verbose=1, **kwargs):
        '''
        train model with a generator
        ----------------------------------
        generator: train generator for training model, Keras ImageDataGenerator is also approved
        batch_size: batch of size
        epochs
        validation_generator: wheather use validation or not, Keras ImageDataGenerator is also approved
        callbacks: list, callable functions
        -----------------------------------
        Return:
        history
        '''
        
        pass
    
    def evaluate_generator(self, generator, batch_size, verbose=0, **kwargs):
        '''
        evaluate model
        return score which has loss and accuracy
        '''
        pass

    def predict_generator(self, generator, batch_size=1, **kwargs):

        pass

    def single_predict(self, item, **kwargs):

        pass
        

class BaseModelBuilder(ABC):
    def __init__(self, **kwargs):
        super(BaseModelBuilder, **kwargs).__init__(**kwargs)
        self.model = None

    def build(self, **kwargs):
        ''''''
        pass


    


    