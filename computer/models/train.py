import os
import sys
import tensorflow as tf
import nvidiaconvnet as model
import load_data

# General training script for tensorflow models

SAVEDIR = "./save"

if __name__=='__main__':
    if not len(sys.argv) == 2:
        print 'Error: incorrect # of arguments'
        print 'Usage: python train.py [train_dir]'


    sess = tf.InteractiveSession()

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(model.y, model._y))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)
    correct_prediction = tf.equal(model.y, model._y)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess.run(tf.initialize_all_variables())

    saver = tf.train.Saver()

    for i in range(10000):
        batch = load_data.getBatch(sys.argv[1], 100)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict = {
                _y: batch[0], x: batch[1], keep_prob:1.0})
            print "step %d, training accuracy %g" % (i, train_accuracy)
            
            if not os.path.exists(SAVEDIR):
                os.makedirs(SAVEDIR)
            checkpoint_path = os.path.join(SAVEDIR, "model.checkpoint")
            filename = saver.save(sess, checkpoint_path)
        train_step.run(feed_dict={_y: batch[0], x: batch[1], keep_prob: 0.5})

    # Do evaluation on evaluation set?
