import keras.backend as K
import numpy as np
import cv2
from skimage.transform import resize

def visualize_cam(model, image, last_conv_layer_index, learning_phase=0, path_to_save=None):
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

    '''Get weights of dense output layer'''
    class_weights = model.layers[-3].get_weights()[0]

    '''Create the function to get last conv layer output and model output'''
    last_conv_layer = model.layers[last_conv_layer_index].output
    get_output = K.function([model.input, K.learning_phase()], [last_conv_layer, model.output])
    img = image
#     img = np.array([np.transpose(np.float32(image), (0, 1, 2))])
    # img = np.asarray(image, dtype='float')
    # if np.max(img) > 1:
    #     img /= 255.
        
    # img = np.expand_dims(img, axis=0)

    [conv_outputs, predictions] = get_output([img, learning_phase])
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


def stack_images(frame, faces, cams):
    if faces is None or len(faces)==0 or cams is None or len(cams)==0:
        return frame
    
    n_faces = len(faces)
    n_cams = len(cams)
    
    frame = np.asarray(frame)
    faces = np.asarray(faces)
    cams = np.asarray(cams)
    
    if np.max(faces) <= 1:
        faces = np.asarray(faces*255, dtype=np.uint8)
    if np.max(cams) <= 1:
        cams = np.asarray(cams*255, dtype=np.uint8)
    
    # convert grayscale 1-D to grayscale 3-D
    if len(faces[0].shape) == 2:
        faces = np.array([np.expand_dims(k, axis=-1) for k in faces])

    if faces[0].shape[-1] == 1:
        faces = np.array([cv2.cvtColor(k, cv2.COLOR_GRAY2BGR) for k in faces])
        

    # resize faces and cams into one size
    h_face = np.mean(np.array([k.shape[0] for k in faces]))
    w_face = np.mean(np.array([k.shape[1] for k in faces]))
    
    faces = np.array([resize(k, (h_face, w_face)) for k in faces])
    cams = np.array([resize(k, (h_face, w_face)) for k in cams])
    
    
    if np.max(faces) <= 1:
        faces = np.asarray(faces*255, dtype=np.uint8)
    if np.max(cams) <= 1:
        cams = np.asarray(cams*255, dtype=np.uint8)
    
    face_stack = np.hstack(faces)
    cam_stack = np.hstack(cams)
    fc_stack = np.vstack([face_stack, cam_stack])
    
    
    info_stack = np.zeros((frame.shape[0], fc_stack.shape[1], 3))
    info_stack[0:fc_stack.shape[0], :, :] = fc_stack
    
    rs = np.hstack([frame, info_stack])
    
    return rs
    
    