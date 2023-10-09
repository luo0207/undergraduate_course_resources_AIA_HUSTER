import tensorflow as tf

# x = tf.constant([[1.0, 1.0, 1],
#                  [2, 2, 2.0]])
# y = tf.constant([1,
#                  1],dtype=tf.int64)
# l = 1
# num_cls = 2

def Loss_ASoftmax(x, y, l, num_cls, m=2, name='asoftmax'):
    '''
    x: B x D - data
    y: B x 1 - label
    l: 1 - lambda
    '''
    xs = x.get_shape()
    print(xs)
    #这里换了一下初始化的
    #w.shape = [features, 2] 2代表着2分类问题  第一个参数指定了变量名称：已有变量或新变量
    w = tf.compat.v1.get_variable("asoftmax/W", [xs[1], num_cls], dtype=tf.float32,
                                  initializer=tf.keras.initializers.glorot_normal())

    eps = 1e-8
    xw = tf.matmul(x, w)
    if m==0:
        return xw, tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=xw))
    #xw = [num, 2类]
    w_norm = tf.norm(w, axis=0) +eps #去掉模的影响 norm计算二范数 axis=0代表每一列求
    logits = xw/w_norm #logits是去掉w模长后的值

    if y is None:
        return logits, None

    ordinal = tf.constant(list(range(0, xs[0])), tf.int64)
    print(y, ordinal)

    ordinal_y = tf.stack([ordinal, y], axis=1)
    x_norm = tf.norm(x, axis=1) + eps
    #logits = [num, 2]
    #这一步就是提取对应类的logits
    sel_logits = tf.gather_nd(logits, ordinal_y) #根据构造出来的索引来提取logits中的元素

    cos_th = tf.divide(sel_logits, x_norm)#找到对应的cos-theta

    if(m==1):
        loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits))
    elif(m==2):
        cos_sign = tf.sign(cos_th)
        #mutiply相同位置的元素相乘
        res = 2 * tf.multiply(tf.sign(cos_th), tf.square(cos_th)) - 1
    elif(m==4):
        cos_th2 = tf.square(cos_th)
        cos_th4 = tf.pow(cos_th, 4)
        sign0 = tf.sign(cos_th)
        sign3 = tf.multiply(tf.sign(2 * cos_th2 - 1), sign0)
        sign4 = 2 * sign0 + sign3 - 3
        res = sign3 * (8 * cos_th4 - 8 * cos_th2 + 1) + sign4 #应该是2sign4？？？
    else:
        raise ValueError('unsupported value of m')

    scaled_logits = tf.multiply(res, x_norm)
    f = 1.0/(1.0 + l)
    ff = 1.0 - f
    # 计算出改变了对应类的seita后的。
    comb_logits_diff = tf.add(logits, tf.scatter_nd(ordinal_y, tf.subtract(scaled_logits, sel_logits), logits.get_shape()))
    update_logits = ff * logits + f * comb_logits_diff
    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=update_logits))

    return  logits,loss

# a, b = Loss_ASoftmax(x, y, l, num_cls, m=4)
# print(a, b)