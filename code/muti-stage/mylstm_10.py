import random

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import data
import os
import logging
from Loss_ASoftmax import Loss_ASoftmax
os.environ['CUDA_VISIBLE_DIVICES'] = '0'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def next_batch(images, sign, num): #生成每个batch的数据
    data1 = images
    data2 = sign
    idx = np.arange(0, len(data1))
    np.random.shuffle(idx)
    idx = idx[0: num]
    data_shuffle1 = np.asarray([data1[i] for i in idx])
    data_shuffle2 = np.asarray([int(data2[i]) for i in idx])
    return data_shuffle1, data_shuffle2, idx

#分出验证级
sess = tf.compat.v1.Session() #搭建tensorflow中对象执行的环境
images, sign = data.data_input("data_LBP_differ/train_zuo.mat")
# images, sign = data.data_input("data_LBP_differ/train_you.mat")
logger.info('images.shape:')
logger.info(images.shape)
pos_images, neg_images = images[:240], images[240:]
random.shuffle(pos_images), random.shuffle(neg_images)
images = np.vstack([pos_images, neg_images]) #240pos 182neg
train_images ,train_sign = np.vstack([images[0:200], images[240:390]]), np.vstack([sign[0:200], sign[240:390]])
valid_images, valid_sign = np.vstack([images[200:240], images[390:]]), np.vstack([sign[200:240], sign[390:]])

#避免麻烦直接把train的数据继续赋值给images
images, sign = train_images, train_sign
#学习率
tf.compat.v1.disable_eager_execution() # It can be used at the beginning of the program for complex migration projects from TensorFlow 1.x to 2.x.
learning_rate = tf.compat.v1.placeholder(tf.float32, shape=None)
def ache_rate(step):
    if(step<100):
        lr = 1e-2
    elif(step<3000):
        lr = 1e-3
    elif(step<30000):
        lr = 1e-4
    elif(step<60000):
        lr = 1e-5
    else:
        lr = 1e-6
    return lr

#参数定义
#placeholder是占位符，相当于定义了一个变量，提前分配了需要的内存。但只有启动一个session，程序才会真正的运行。建立session后，通过feed_dict()函数向变量赋值。
batch_size = tf.compat.v1.placeholder(tf.int32, [])
input_size = 118
timestep_size = 9
hidden_size = 128
layer_num = 2
# class_num = 1

_batch_size = 4
X = tf.compat.v1.placeholder(tf.float32, [_batch_size, timestep_size, input_size])#[batch*frames*features]
y = tf.compat.v1.placeholder(tf.int64, [_batch_size])#[batch]

keep_prob = tf.compat.v1.placeholder(tf.float32, [])#遗忘的参数定义

#LSTM10
def getcell(hidden_size, keep_prob):
    lstm_cell = tf.compat.v1.nn.rnn_cell.BasicLSTMCell(num_units=hidden_size, forget_bias=1.0, state_is_tuple=True)#128个lstm单元 遗忘门偏置为1  accepted and returned states are 2-tuples of the c_state and m_state.
    lstm_cell = tf.compat.v1.nn.rnn_cell.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=keep_prob)# no input dropout will be added. no output dropout will be added.
    return lstm_cell
#M-LSTM
mlstm_cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell([getcell(hidden_size, keep_prob) for _ in range(layer_num)], state_is_tuple=True)
#初始化 [2*4*128]
init_state = mlstm_cell.zero_state(_batch_size, dtype=tf.float32)
outputs = list()
state = init_state

with tf.compat.v1.variable_scope('RNN'): #This context manager validates that the (optional) values are from the same graph, ensures that graph is the default graph, and pushes a name scope and a variable scope.
    for timestep in range(timestep_size):
        if timestep>0:
            #Returns the current variable scope.
            tf.compat.v1.get_variable_scope().reuse_variables() #计算图复用
        (cell_output, state) = mlstm_cell(X[:, timestep, :], state)
        outputs.append(cell_output)
#隐层状态输出
h_state_1 = outputs[-1]
h_state_2 = outputs[-1 - 1]
h_state = tf.concat([h_state_1, h_state_2], 1)
print("hstate:%s" % h_state)

#损失函数
logits, cross_entropy = Loss_ASoftmax(x = h_state, y=y, l=1.0, num_cls=2, m=4 )
train_op = tf.compat.v1.train.AdamOptimizer(learning_rate,beta1=0.5,beta2=0.9).minimize(cross_entropy)
res = tf.argmax(logits, 1)
saver = tf.compat.v1.train.Saver(max_to_keep=750)
sess.run(tf.compat.v1.global_variables_initializer())

train_accs = []
train_losses = []
train_acc = 0
train_loss = 0
for j in range(75000):#472
    lrn_rate = ache_rate(j)
    train_x, train_y, idx = next_batch(images, sign, _batch_size)
    train_error = sess.run(cross_entropy, feed_dict={X: train_x, y: train_y, keep_prob: 1.0, batch_size: _batch_size, learning_rate: lrn_rate})
    train_loss += train_error
    res_ = sess.run(res, feed_dict={X: train_x, y: train_y, keep_prob: 1.0, batch_size: _batch_size,learning_rate:lrn_rate})
    print("res:", res_)
    print("true:", train_y)
    train_acc = train_acc + np.sum(res_==train_y)
    sess.run(train_op, feed_dict={X: train_x, y: train_y, keep_prob: 0.5, batch_size: _batch_size,learning_rate:lrn_rate})
    if((j+1)%100 ==0):
        saver.save(sess, 'model_LBP_differ/zuo/10lstm.ckpt', global_step=j + 1)
        logger.info("step %d, training error %g,learning_rate:%g" % ((j+1), train_error, lrn_rate))
        train_accs.append(train_acc*100/400)
        train_losses.append(train_loss)
        train_acc, train_loss = 0, 0

#做loss可视化
plt.subplot(1, 2, 1)
plt.plot(train_accs)
plt.title('accuracy-epoch')
plt.xlabel("epoch")
plt.ylabel("accuracy")

plt.subplot(1, 2, 2)
plt.plot(train_losses)
plt.title('loss-epoch')
plt.xlabel("epoch")
plt.ylabel("loss")

plt.show()

