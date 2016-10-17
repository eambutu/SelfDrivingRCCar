import tensorflow as tf
import random

training_x = []
training_y = []
# Load the training data here
#
#

# Creating model
# Replace 100 with dimensions
x = tf.placeholder(tf.float32, [None, 100])
W = tf.Variable(tf.zeros([100, 5]))
b = tf.Variable(tf.zeros([5]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

# Define placeholder for correct values
y_ = tf.placeholder(tf.float32, [None, 5])
# Define cost function
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
# Define train step
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Define init step
init = tf.initialize_all_variables()

# Launch model in session, run init
sess = tf.Session()
sess.run(init)

def getNextBatch(size):
    indices = random.sample(range(0, num_samples), size)
    xs_test = [training_x[i] for i in indexes]
    ys_test = [training_y[i] for i in indexes]
    return xs_test, ys_test

# Run 1000 iterations of training step
for i in range(1000):
    if (i % 100 == 0):
        print(i)
    batch_xs, batch_ys = getNextBatch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# create Saver object to save your variables
saver = tf.train.Saver()

# save at iteration "global step"
saver_def = saver.as_saver_def()
print saver_def.filename_tensor_name
print saver_def.restore_op_name

# write out three files
saver.save(sess, 'trained_model.sd')
tf.train.write_graph(sess.graph_def, '.', 'trained_model.proto', as_text=False)
tf.train.write_graph(sess.graph_def, '.', 'trained_model.txt', as_text=True)
