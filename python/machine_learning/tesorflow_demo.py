#-*-coding:utf-8-*-
import os
import sys

import tensorflow as tf
from datasets import datasets


#reload(sys)
#sys.setdefaultencoding("utf-8")


def get_unique_id(self, data_dir):
    dir_list = data_dir.split("/")
    class_id = dir_list[2].split("_")[0]
    text_id = dir_list[4].split(".")[0]
    type_id = dir_list[1].split("_")[0]
    return class_id + "_" + type_id + "_" + text_id



data_sets = datasets()
data_sets.read_train_data(".", True)
sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, [None, 5000])
W = tf.Variable(tf.zeros([5000, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = -tf.reduce_sum(y_ * tf.log(y + 1e-10))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

#training
tf.global_variables_initializer().run()
saver = tf.train.Saver()
for i in range(1000):
    batch_xs, batch_ys = data_sets.train.next_batch(100)
    train_step.run({x: batch_xs, y_: batch_ys})
print (W.eval())
print (b.eval())
path = saver.save(sess, "./model2/model.md")