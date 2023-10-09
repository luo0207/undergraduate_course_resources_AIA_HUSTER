import tensorflow as tf
import h5py
import numpy as np
import time
import data
import os
import scipy.io as scio
from Loss_ASoftmax import Loss_ASoftmax
os.environ["CUDA_VISIBLE_DEVICES"] = '1'
tf.compat.v1.disable_eager_execution()
batch_size = tf.compat.v1.placeholder(tf.int32,[])
label_mat = h5py.File("label_zuo.mat")
label_test=label_mat['label'][:]

def getcell(hidden_size):
    lstm_cell = tf.compat.v1.nn.rnn_cell.BasicLSTMCell(num_units=hidden_size, forget_bias=1.0, state_is_tuple=True)
    lstm_cell = tf.compat.v1.nn.rnn_cell.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=1.0)
    return lstm_cell

with tf.compat.v1.Session() as sess:
    i = 19
    _batch_size = 221
    # _batch_size = 224
    images, sign = data.test_input("data_LBP_differ/test_zuo.mat", _batch_size)
    model_file = "model_LBP_differ/zuo/"
    # images, sign = data.test_input("data_LBP_differ/test_you.mat", _batch_size)
    # model_file = "model_LBP_differ/you/"
    print("sign:{},images:{}".format(np.shape(sign), np.shape(images)))
    input_size = 118
    timestep_size = 9  # each prediction need 28 samples
    hidden_size = 128  # number of hidden layres
    layer_num = 2  # LSTM layer number
    class_num = 1  # class of output .should be 1 if regression
    X = tf.compat.v1.placeholder(tf.float32, [_batch_size, timestep_size, input_size])
    y = tf.compat.v1.placeholder(tf.int64, [_batch_size])

    # M-LSTM
    mlstm_cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell([getcell(hidden_size) for _ in range(layer_num)],state_is_tuple=True)
    # 0初始化
    init_state = mlstm_cell.zero_state(_batch_size, dtype=tf.float32)
    outputs = list()
    state = init_state

    with tf.compat.v1.variable_scope('RNN'):
        for timestep in range(timestep_size):
            if timestep > 0:
                tf.compat.v1.get_variable_scope().reuse_variables()  # 计算图复用
            (cell_output, state) = mlstm_cell(X[:, timestep, :], state)
            outputs.append(cell_output)
    # 隐层状态输出
    h_state_1 = outputs[-1]
    h_state_2 = outputs[-1 - 1]
    h_state = tf.concat([h_state_1, h_state_2], 1)
    print("hstate:%s" % h_state)

    TP, TN, FP, FN = 0, 0, 0,0
    # 损失函数
    logits, cross_entropy = Loss_ASoftmax(x=h_state, y=y, l=1.0, num_cls=2, m=4)
    res = tf.argmax(logits, 1)
    saver = tf.compat.v1.train.Saver(max_to_keep=100)
    path = "model_LBP_differ/zuo/10lstm.ckpt_allAsoftmax--" + str(40000)
    # path = "model_LBP_differ/you/10lstm.ckpt-" + str(50000)
    saver.restore(sess, path)
    # saver.restore(sess, 'model_LBP_differ/zuo/10lstm.ckpt-421')
    res_ = sess.run(res, feed_dict={X: images, y: sign, batch_size: _batch_size})

    # print("process1")
    for i in range(len(sign)):
        if(sign[i]==1 and res_[i]==1):
            TP += 1
        elif(sign[i]==1 and res_[i]==0):
            FN += 1
        elif(sign[i]==0 and res_[i]==1):
            FP += 1
        else:
            TN += 1
    recall = TP/(TP+FN)
    precision = TP/(TP+FP)
    F1score = 2*recall*precision/(recall+precision)
    print(f"-------------------left-test------------------,使用的权重文件为：batchsizes:{60000}")
    print("测试级准确度为{:.2f}%".format(np.sum(res_==sign)* 100 / 221)) #左眼
    # print("测试级准确度为{:.2f}%".format(np.sum(res_ == sign) * 100 / 224))
    print("Recall为{:.4f} , precision为{:.4f}, F1score为{:.4f}".format(recall, precision, F1score))
    # str_ = 'data_temporal_test/res_zuo_0.797386.mat'
    # scio.savemat(str_, {'logit': logit, })

    # saver.restore(sess, 'model_LBP_differ/zuo/locate/0.758170lstm.ckpt')
    # logit = sess.run(logits, feed_dict={
    #     X: images, y: sign, batch_size: _batch_size})
    # print("process2")
    # str_ = 'data_temporal_test/res_zuo_0.758170.mat'
    # scio.savemat(str_, {'logit': logit, })
    #
    # saver.restore(sess, 'model_LBP_differ/zuo/locate/0.732026lstm.ckpt')
    # logit = sess.run(logits, feed_dict={
    #     X: images, y: sign, batch_size: _batch_size})
    # print("process3")
    # str_ = 'data_temporal_test/res_zuo_0.732026.mat'
    # scio.savemat(str_, {'logit': logit, })
    #
    # saver.restore(sess, 'model_LBP_differ/zuo/locate/10lstm.ckpt-50000')
    # logit = sess.run(logits, feed_dict={
    #     X: images, y: sign, batch_size: _batch_size})
    #
    # print("process4")
    # str_ = 'data_temporal_test/res_zuo_15400.mat'
    # scio.savemat(str_, {'logit': logit, })
