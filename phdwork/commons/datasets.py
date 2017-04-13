from keras.datasets import mnist
from phdwork.metagenome.preprocessing import *

import numpy as np
import scipy.io as sio
import pandas as pd

def load_mnist(order='th'):

    # input image dimensions
    img_rows, img_cols, img_channels,  = 28, 28, 1

    if order == 'tf':
        input_shape=(img_rows, img_cols, img_channels)
    elif order == 'th':
        input_shape=(img_channels, img_rows, img_cols)

    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    X_train = X_train.reshape(len(X_train), input_shape[0], input_shape[1], input_shape[2])
    X_test = X_test.reshape(len(X_test), input_shape[0], input_shape[1], input_shape[2])

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    return (X_train, y_train), (X_test, y_test), input_shape


def load_svhn(order='th', path=None):

    # input image dimensions
    img_rows, img_cols, img_channels,  = 32, 32, 3
    nb_classes = 10

    if order == 'tf':
        input_shape=(img_rows, img_cols, img_channels)
    elif order == 'th':
        input_shape=(img_channels, img_rows, img_cols)

    if path is None:
        train_data = sio.loadmat('/home/ozsel/Jupyter/datasets/svhn/train_32x32.mat')
    else:
        train_data = sio.loadmat(path + 'train_32x32.mat')

    # access to the dict
    X_train = train_data['X']
    X_train = X_train.reshape(img_channels*img_rows*img_cols, X_train.shape[-1]).T
    X_train = X_train.reshape(len(X_train), input_shape[0], input_shape[1], input_shape[2])
    X_train = X_train.astype('float32')
    X_train /= 255

    y_train = train_data['y']
    y_train = y_train.reshape(len(y_train))
    y_train = y_train%nb_classes

    del train_data

    if path is None:
        test_data = sio.loadmat('/home/ozsel/Jupyter/datasets/svhn/test_32x32.mat')
    else:
        test_data = sio.loadmat(path + 'test_32x32.mat')

    # access to the dict
    X_test = test_data['X']
    X_test = X_test.reshape(img_channels*img_rows*img_cols, X_test.shape[-1]).T
    X_test = X_test.reshape(len(X_test), input_shape[0], input_shape[1], input_shape[2])
    X_test = X_test.astype('float32')
    X_test /= 255

    y_test= test_data['y']
    y_test = y_test.reshape(y_test.shape[0])
    y_test = y_test%nb_classes

    del test_data

    return (X_train, y_train), (X_test, y_test), input_shape


def load_norb(order='th', path=None, use_pairs=False):

    # input image dimensions
    img_rows, img_cols, img_channels,  = 96, 96, 1

    if order == 'tf':
        input_shape=(img_rows, img_cols, img_channels)
    elif order == 'th':
        input_shape=(img_channels, img_rows, img_cols)

    if path is None:
        X_train = np.load('/home/ozsel/Jupyter/datasets/norb/X_train.npy')
        y_train = np.load('/home/ozsel/Jupyter/datasets/norb/y_train.npy')
    else:
        X_train = np.load(path + 'X_train.npy')
        y_train = np.load(path + 'y_train.npy')

    if use_pairs:
        X_train = X_train.reshape(len(X_train)*2, input_shape[0], input_shape[1], input_shape[2])
    else:
        X_train = X_train[:,0,]
        X_train = X_train.reshape(len(X_train), input_shape[0], input_shape[1], input_shape[2])

    X_train = X_train.astype('float32')
    X_train /= 255


    if use_pairs:
        y_train = np.stack((y_train, y_train),axis=-1).reshape(len(y_train)*2,)

    if path is None:
        X_test = np.load('/home/ozsel/Jupyter/datasets/norb/X_test.npy')
        y_test = np.load('/home/ozsel/Jupyter/datasets/norb/y_test.npy')
    else:
        X_test = np.load(path + 'X_test.npy')
        y_test = np.load(path + 'y_test.npy')

    if use_pairs:
        X_test = X_test.reshape(len(X_test)*2, input_shape[0], input_shape[1], input_shape[2])
    else:
        X_test = X_test[:,0,]
        X_test = X_test.reshape(len(X_test), input_shape[0], input_shape[1], input_shape[2])
    X_test = X_test.astype('float32')
    X_test /= 255


    if use_pairs:
        y_test = np.stack((y_test, y_test),axis=-1).reshape(len(y_test)*2,)

    return (X_train, y_train), (X_test, y_test), input_shape


def load_sar11(path=None, label_type='parent', miniseqs_size=2000, nb_pseudos=100):

    nb_classes = 75

    if label_type == 'pseudo_complete' or label_type == 'pseudo_mini':
        loc = '/home/ozsel/Jupyter/datasets/metagenome/metagenome75'
    elif 'parent':
        loc = '/home/ozsel/Jupyter/datasets/metagenome/metagenome75_sparse.csv'
    df = pd.read_csv(loc, header=0, sep=',')

    if label_type == 'pseudo_complete':
        X = get_pseudo_labels_comlete(df, nb_classes, nb_pseudos)
    elif label_type == 'pseudo_mini':
        X = get_pseudo_labels_mini(df, nb_classes, miniseqs_size, nb_pseudos)
    elif label_type == 'parent':
        X = get_parent_labels_wrt_gene_call(df, nb_classes)
        nb_pseudos=X.shape[0]/nb_classes

    np.random.shuffle(X)

    X_train = X[:,:,[3,4]].reshape(X.shape[0], X.shape[1]*2)
    X_train = X_train.astype('float32')
    X_train = (X_train)/21

    y_train_pseudo = X[:,0,1]
    y_train = X[:,0,0]

    input_shape = (X_train.shape[1],)

    return (X_train, y_train, y_train_pseudo), nb_pseudos, input_shape
