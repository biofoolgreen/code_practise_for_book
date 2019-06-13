'''
@Description: TensorFlow-实战Google深度学习框架
@Version: 
@Author: liguoying
@Date: 2019-06-13 11:07:23
'''
#################
# 实现LeNet-5模型#
#################
"""
Architecture:
---
    Conv1:
        input:      32x32x1
        filter:     5x5x6
        padding:    no padding
        stride:     1x1
        output:     28x28x6
    
    Pool1:
        input:      28x28x6
        filter:     2x2
        stride:     2x2
        output:     14x14x6
    
    Conv2:
        input:      14x14x6
        filter:     5x5x16
        padding:    no padding
        stride:     1x1
        output:     10x10x16
    
    Pool2:
        input:      10x10x16
        filter:     2x2
        stride:     2x2
        output:     5x5x16
    
    Full1:
        input:      5x5x16
        hidden:     120
        output:     120
    
    Full2:
        input:      120
        hidden:     84
        output:     84
    
    Full3:
        input:      84
        output:     10
"""
import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

INPUT_NODE = 32*32
OUTPUT_NODE = 10
IMAGE_SIZE = 28
NUM_CHANNELS = 1
NUM_LABELS = 10

REGULARAZTION_RATE = 0.0001
BATCH_SIZE = 100
LEARNING_RATE = 0.8
LEARNING_RATE_DECAY = 0.99
TRAINING_STEPS = 30000
MOVING_AVERANGE_DECAY = 0.99

MODEL_SAVE_PATH = r'tensorflow-practise_with_deeplearning_framework\models'
MODEL_NAME = "LeNet5_model.ckpt"

def inference(input_tensor, train, regularizer):
    with tf.variable_scope('layer1-conv1'):
        conv1_weights = tf.get_variable(
            "weights", shape=[5, 5, 1, 32],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        conv1_bias = tf.get_variable(
            "bias", shape=[32], initializer=tf.constant_initializer(0.0)
        )

        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_bias))
    
    with tf.variable_scope('layer2-pool1'):
        pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    
    with tf.variable_scope('layer3-conv2'):
        conv2_weights = tf.get_variable(
            "weights", shape=[5, 5, 32, 64],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        conv2_bias = tf.get_variable(
            "bias", shape=[64], initializer=tf.constant_initializer(0.0)
        )

        conv2 = tf.nn.conv2d(input_tensor, conv2_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_bias))
    
    with tf.variable_scope('layer4-pool2'):
        pool2 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")    
    

    pool_shape = pool2.get_shape().as_list()
    # pool_shape = [batch_size, height, width, depth]
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
    reshaped = tf.reshape(pool2, [pool_shape[0], nodes])

    with tf.variable_scope('layer5-fc1'):
        fc1_weights = tf.get_variable(
            "weights", [nodes, 512],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        # 只有全连接层的权重需要加入正则化
        if regularizer is not None:
            tf.add_to_collection('losses', regularizer(fc1_weights))
        
        fc1_bias = tf.get_variable("bias", [512], initializer=tf.constant_initializer(0.1))

        fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_weights) + fc1_bias)
        if train:
            fc1 = tf.nn.dropout(fc1, 0.5)
    
    with tf.variable_scope('layer6-fc2'):
        fc2_weights = tf.get_variable(
            "weights", [512, NUM_LABELS],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        # 只有全连接层的权重需要加入正则化
        if regularizer is not None:
            tf.add_to_collection('losses', regularizer(fc2_weights))
        
        fc2_bias = tf.get_variable("bias", [NUM_LABELS], initializer=tf.constant_initializer(0.1))

        output = tf.nn.relu(tf.matmul(fc1, fc2_weights) + fc2_bias)        

    return output



def train(mnist):
    x = tf.placeholder(tf.float32, [None, 784], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, 10], name='y-input')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)

    y = inference(x, True, regularizer=regularizer)

    global_step = tf.Variable(0, trainable=False)

    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERANGE_DECAY, global_step)
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(y, tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(LEARNING_RATE, global_step, 
                                                mnist.train.num_examples/BATCH_SIZE,
                                                LEARNING_RATE_DECAY)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name='train')
    
    # 初始化tf持久化
    saver = tf.train.Saver()
    with tf.Session() as sess:
        tf.initialize_all_variables().run()

        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x:xs, y_:ys})

            # 每1000轮保存一次
            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)



def main(argv=None):
    mnist = input_data.read_data_sets("tensorflow-practise_with_deeplearning_framework\data", one_hot=True)
    train(mnist)


if __name__ == "__main__":
    tf.app.run(main=main)