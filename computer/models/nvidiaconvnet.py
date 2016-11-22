import tensorflow as tf
import scipy

# Convolutional neural network, as outlined by NVIDIA paper
# 27 million connections and 250 thousand parameters

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding='VALID')

# Height: 144, width: 176
x = tf.placeholder(tf.float32, shape=[None, 144, 176, 1])
y_ = tf.placeholder(tf.float32, shape=[None, 4])

# First convolutional layer
# Dimensions after: 24@70x86
W_conv1 = weight_variable([5, 5, 1, 24])
b_conv1 = bias_variable([24])

h_conv1 = tf.nn.relu(conv2d(x, W_conv1, 2) + b_conv1)

# Second convolutional layer
# Dimensions after: 36@33x41
W_conv2 = weight_variable([5, 5, 24, 36])
b_conv2 = bias_variable([36])

h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2, 2) + b_conv2)

# Third convolutional layer
# Dimensions after: 48@15x19
W_conv3 = weight_variable([5, 5, 36, 48])
b_conv3 = bias_variable([48])

h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 2) + b_conv3)

# Fourth convolutional layer
# Dimensions after: 64@7x9
W_conv4 = weight_variable([3, 3, 48, 64])
b_conv4 = bias_variable([64])

h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4, 1) + b_conv4)

# Fifth convolutional layer
# Dimensions after: 64@3x4
W_conv5 = weight_variable([3, 3, 64, 64])
b_conv5 = bias_variable([64])

h_conv5 = tf.nn.relu(conv2d(h_conv4, W_conv5, 1) + b_conv5)

# First fully connected layer
# (Figure out: should I still be doing 1164? What's special about this num?)
h_conv5_flatten = tf.reshape(h_conv5, [-1])
W_fc1 = weight_variable([764, 1164]) 
b_fc1 = bias_variable([1164])

h_fc1 = tf.nn.relu(tf.matmul(h_conv5_flatten, W_fc1) + b_fc1)

dropout = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, dropout)

# Second fully connected layer
W_fc2 = weight_variable([1164, 100])
b_fc2 = bias_variable([100])

h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

h_fc2_drop = tf.nn.dropout(h_fc2, dropout)

# Third fully connected layer
W_fc3 = weight_variable([100, 50])
b_fc3 = bias_variable([50])

h_fc3 = tf.nn.relu(tf.matmul(h_fc2_drop, W_fc3) + b_fc3)

h_fc3_drop = tf.nn.dropout(h_fc3, dropout)

# Fourth fully connected layer
# (Again, should I be tweaking this?)
W_fc4 = weight_variable([50, 8])
b_fc3 = weight_variable([8])

y = tf.nn.tanh(tf.matmul(h_fc3_drop, W_fc4) + b_fc4)
