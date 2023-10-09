import tensorflow as tf
import os
import h5py
import numpy as np

def data_input(datapath):

    data_mat = h5py.File(datapath) #读出文件中的mat数据
    images = data_mat['data'][:].transpose((0, 2, 1))  #(batch, frame, feature)
    sign = data_mat['label'][:].transpose((1, 0)) #(batch, 1)
    return images, sign

def test_input(datapath, _batch_size):
    data_mat = h5py.File(datapath)
    images_ = data_mat['data'][:].transpose((0, 2, 1))
    sign_ = data_mat['label'][:].transpose((1, 0))
    images = np.asarray([images_[i] for i in range(_batch_size)])
    sign = np.asarray([int(sign_[i]) for i in range(_batch_size)])
    return images, sign
