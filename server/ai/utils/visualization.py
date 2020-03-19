import keras.backend as K
import numpy as np
import cv2
from skimage.transform import resize
import tensorflow as tf

global graph
graph = tf.get_default_graph()

def visualize_cam(model, func, image, path_to_save=None):
    '''
  visualize class activation map function
  ----------------------------------------
  arguments:
  - model: Keras model instance with average pooling layer
  - image: image to apply cam
  - last_conv_layer_index: index of last convolution layer
  - learning_phase: integer, if 1 then mode='learing', else if 0 then mode='testing'
  - path_to_save: path to save the image
  -----------------------------------------
  return:
    predictions: softmax vector
  '''
    with graph.as_default():

        '''Get weights of dense output layer'''
        class_weights = model.layers[-3].get_weights()[0]

        '''Create the function to get last conv layer output and model output'''
        # last_conv_layer = model.layers[last_conv_layer_index].output
        # get_output = K.function([model.input, K.learning_phase()], [last_conv_layer, model.output])
        img = image
    #     img = np.array([np.transpose(np.float32(image), (0, 1, 2))])
        # img = np.asarray(image, dtype='float')
        # if np.max(img) > 1:
        #     img /= 255.

        # img = np.expand_dims(img, axis=0)

        [conv_outputs, predictions] = func([img, 0])

        conv_outputs = conv_outputs[0,:,:,:]

        '''Create the class activation map'''
        class_num = np.argmax(predictions, axis=1)[0]
        prob = np.max(predictions, axis=1)[0]
        cam = np.zeros(dtype=np.float32, shape=conv_outputs.shape[:2])

        for i,w in enumerate(class_weights[:,class_num]):
            cam += w*conv_outputs[:,:,i]
        cam /= np.max(cam)
        cam = resize(cam, (image.shape[0], image.shape[1]))
        
        cam = np.asarray(cam*255, dtype=np.uint8)
        cam = np.clip(cam, 0, 255)
        cam = cv2.applyColorMap(255-cam, cv2.COLORMAP_JET)
        
        if path_to_save is not None:
            plt.savefig(path_to_save)
            
        return class_num, prob, cam

def preprocess_uint8(image):
    image = np.asarray(image)

    if np.max(image) <= 1:
        return np.asarray(image*255, dtype=np.uint8)
    return np.asarray(image, dtype=np.uint8)

def stack_images(frame, faces, cams, shape=(1000,1000,3)):
    rs = np.zeros(shape)
    frame = preprocess_uint8(frame)

    if faces is None or cams is None or len(faces) == 0:
        rs[0:frame.shape[0], 0:frame.shape[1], :] = frame
        rs = np.asarray(rs, dtype=np.uint8)
        return rs

    
    faces = preprocess_uint8(faces)
    cams = preprocess_uint8(cams)
    
    
    h = np.mean(np.array([k.shape[0] for k in faces]))
    w = np.mean(np.array([k.shape[1] for k in faces]))
  
    
    # expand dims if needed
    if len(faces[0].shape)==2:
        faces = [np.expand_dims(k, axis=-1) for k in faces]
    if len(cams[0].shape)==2:
        cams = [np.expand_dims(k, axis=-1) for k in cams]
    
    # convert to 3-D
    if faces[0].shape[-1] == 1:
        faces = [cv2.cvtColor(k, cv2.COLOR_GRAY2BGR) for k in faces]
    if cams[0].shape[-1] == 1:
        cams = [cv2.cvtColor(k, cv2.COLOR_GRAY2BGR) for k in cams]
    
    # resize
    faces = [resize(k, (h,w)) for k in faces]
    cams = [resize(k, (h,w)) for k in cams]
    
    # preprocessing
    frame = preprocess_uint8(frame)
    faces = preprocess_uint8(faces)
    cams = preprocess_uint8(cams)
    
    fc_stack = np.hstack(faces)
    cm_stack = np.hstack(cams)
    info_stack = np.vstack([fc_stack, cm_stack])
    
    rs[0:frame.shape[0], 0:frame.shape[1], :] = frame
    rs[0: info_stack.shape[0], -info_stack.shape[1]:, :] = info_stack
    
    rs = np.asarray(rs, dtype=np.uint8)
   
    return rs
    
    
    
