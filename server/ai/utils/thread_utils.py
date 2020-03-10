import threading
from abc import ABC


class ThreadHandler(ABC):
    '''Manage all thread defined by classes'''

    def __init__(self, **kwargs):
        super(ThreadHandler, self).__init__(**kwargs)
        self._threads = []


class BaseThread(threading.Thread):
    def __init__(self, thread_handler, target_func, *args, **kwargs):
        super(BaseThread, self).__init__(**kwargs)
        self.thread_handler = thread_handler
        self._target_func = target_func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        self._target(*self._args, **self._kwargs)


class TrainingThread(BaseThread):
    '''
    Class handle thread for training.
    ----------------------------------------
    thread_handler: ThreadHandler object
    target_func: fit function for training
    *args: arguments for target_function
    **kwargs: arguments for target_function
    '''

    def __init__(self, thread_handler, target_func, *args, **kwargs):
        super(TrainingThread, self).__init__(
            thread_handler, target_func, *args, **kwargs)


class UploadingThread(threading.Thread):
    '''
    Class handle thread for uploading data.
    ----------------------------------------
    target_func: upload function for data
    *args: arguments for target_function
    **kwargs: arguments for target_function
    '''
    def __init__(self, thread_handler, target_func, *args, **kwargs):
        super(UploadingThread, self).__init__(thread_handler, target_func, *args, **kwargs)

class EvaluatingThread(threading.Thread):
    '''
    Class handle thread for evaluating model.
    ----------------------------------------
    target_func: evaluate model function
    *args: arguments for target_function
    **kwargs: arguments for target_function
    '''
    def __init__(self, thread_handler, target_func, *args, **kwargs):
        super(EvaluatingThread, self).__init__(thread_handler, target_func, *args, **kwargs)



