import os
import keras.backend as K
import tensorflow as tf
import keras
from keras.models import load_model
import tensorflow
from skimage.transform import resize
import numpy as np
import pickle

dirname = os.path.dirname(__file__)
print(dirname)
root_path = os.path.join(dirname, 'data')

#call
def load_face_demo_model():
    return load_model(os.path.join(dirname, './demo_face_model.hdf5'))

# call
def predict_fomular_model(images, r, alpha, beta, gamma, delta, e_s, e_b, dataset_id):
    '''
    predict for images with specified model
    --------------------------------------------
    return
        labels, accuracies, history
    '''
    K.clear_session()
    images = preprocess_image(images)

    # find the size M, N
    M = images.shape[1]

    predict_model, history, (M_s, N_s) = load_model_by_size(M, r, alpha, beta, gamma, delta, e_s, e_b, dataset_id)

    # interpolate image by size
    print(images.shape)
    rs_images = []
    for i in range(images.shape[0]):
        rs_images.append(resize(images[i], (M_s, N_s)))
    
    rs_images = np.asarray(rs_images, dtype='float64')
    preds = predict_model.predict(rs_images, verbose=0)
    
    return np.argmin(preds, axis=1), np.max(preds, axis=1), history, (M_s, N_s)

# call
def predict_original_model(images, r, alpha, beta, gamma, delta, e_s, e_b, dataset_id):
    '''
    predict for images with specified model
    --------------------------------------------
    return
        labels, accuracies
    '''
    K.clear_session()
    # preprocess r, alpha, beta, gamma, delta, e_s, e_b
    r_str = "{0:.4f}".format(round(r,4))
    alpha_str =  "{0:.4f}".format(round(alpha,4))
    beta_str =  "{0:.4f}".format(round(beta,4))
    gamma_str =  "{0:.4f}".format(round(gamma,4))
    delta_str =  "{0:.4f}".format(round(delta,4))
    e_s_str =  "{0:.4f}".format(round(e_s,4))
    e_b_str =  "{0:.4f}".format(round(e_b,4))
    
    fomulars = os.listdir(root_path)

    direct = r_str +'_' + alpha_str +'_' + beta_str +'_' + gamma_str +'_' + delta_str +'_' + e_s_str +'_' + e_b_str + '_' + dataset_id
    if direct in fomulars:
        model_path = os.path.join(root_path, direct, 'models', 'original_model.h5py')

    images = preprocess_image(images)
    
    original_model = load_model(model_path)
    print(original_model.inputs)

    interpolated_imgs = []
    for i in range(images.shape[0]):
        i_images = interpolate_image(images[i], (int(original_model.inputs[0].shape[1]), int(original_model.inputs[0].shape[2])))
        interpolated_imgs.append(i_images)
    
    interpolated_imgs = np.asarray(interpolated_imgs)
    interpolated_imgs = np.concatenate(interpolated_imgs, axis=0)
    
    preds = original_model.predict(interpolated_imgs, verbose=0)
    return np.argmax(preds, axis=1), np.max(preds, axis=1), interpolated_imgs


def preprocess_image(images):
    images = np.asarray(images, dtype='float64')
    images = np.expand_dims(images, axis=-1)
       
    for image in images:
        if np.max(image) > 1:
            image /= 255
    return images

def load_model_by_size(M, r, alpha, beta, gamma, delta, e_s, e_b, dataset_id):
    '''
    load model and history by size M

    return model, size
    '''
    # preprocess r, alpha, beta, gamma, delta, e_s, e_b
    r_str = "{0:.4f}".format(round(r,4))
    alpha_str =  "{0:.4f}".format(round(alpha,4))
    beta_str =  "{0:.4f}".format(round(beta,4))
    gamma_str =  "{0:.4f}".format(round(gamma,4))
    delta_str =  "{0:.4f}".format(round(delta,4))
    e_s_str =  "{0:.4f}".format(round(e_s,4))
    e_b_str =  "{0:.4f}".format(round(e_b,4))
    
    fomulars = os.listdir(root_path)
    print('fomulars:', fomulars)
    direct = r_str +'_' + alpha_str +'_' + beta_str +'_' + gamma_str +'_' + delta_str +'_' + e_s_str +'_' + e_b_str + '_' + dataset_id
    print('direct:', direct)

    if direct in fomulars:
        print(direct)
        # load model by size
        model_paths = os.listdir(os.path.join(root_path, direct, 'models'))
        history_paths = os.listdir(os.path.join(root_path, direct, 'histories'))
        
        M_sizes = []
        N_sizes = []
        
        for k in model_paths:
            if 'original' in k:
                continue
            
            M_sizes.append(int(k.split('_')[0]))
            N_sizes.append(int(k.split('_')[1]))

        min_index = find_cloest_size(M, M_sizes)

        model_path = os.path.join(root_path, direct, 'models', model_paths[min_index])
        history_path = os.path.join(root_path, direct, 'histories', history_paths[min_index])

        print(model_path)
        print(history_path)

        with open(history_path, 'rb') as dt:
            history = pickle.load(dt)

        history['epochs'] = len(history['val_acc'])

        return load_model(model_path), history, (M_sizes[min_index], N_sizes[min_index])

    else:
        return None

def find_cloest_size(M, sizes):
    '''
    find cloest sizes for M
    '''

    dist = np.array([abs(M-k) for k in sizes])
    return np.argmin(dist)

def interpolate_image(image, original_size):
    rs = []
    # nb, bilinear, bicubic

    orders = [0,1,3]
    for i in orders:
        t_image = resize(image, (original_size), order=i)
        rs.append(t_image)

    return rs



# model, history, (_,_) = load_model_by_size(11, 0.2, 2.5, 0.5, 1.0, 0.5, 0, 0, 'ORL')
# print(history)

# model_path = './data/0.2000_2.5000_0.5000_1.0000_0.5000_0.0000_0.0000_ORL/original_model.h5py'
# img_path = './temp_0_2_0.png'

# from skimage.io import imread

# image = imread(img_path)
# image = preprocess_image(image)

# preds, probs = predict_original_model(image, model_path)
# print(preds.shape)
# print(preds)

# print(probs.shape)
# print(probs)

    