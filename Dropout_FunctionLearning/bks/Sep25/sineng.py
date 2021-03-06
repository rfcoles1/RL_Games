import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pylab import savefig

import tensorflow as tf
import tensorflow.contrib.slim as slim

num_hidden = 512
num_batches = 1
drop_rate = 0.5
num_to_predict = 50

seed = 100
np.random.seed(seed)
tf.set_random_seed(seed)

class network():
    def __init__(self):
        self.curr_epoch = 0
 
        self.data = tf.placeholder(tf.float32, [None,1])
        self.target = tf.placeholder(tf.float32, [None,1])
        self.keep_prob = tf.placeholder(tf.float32)
        
        #tf.contrib.layers.xavier_initializer()
        #tf.contrib.layers.variance_scaling_initializer()
        self.fc1 = slim.fully_connected(self.data, num_hidden,
            activation_fn = tf.nn.relu,
            weights_initializer = tf.contrib.layers.xavier_initializer(),
            biases_initializer = tf.ones_initializer())
        self.drop1 = tf.nn.dropout(self.fc1, self.keep_prob)
        self.fc2 = slim.fully_connected(self.drop1, num_hidden,
            activation_fn = tf.nn.relu,
            weights_initializer = tf.contrib.layers.xavier_initializer(),
            biases_initializer = tf.zeros_initializer())
        self.drop2 = tf.nn.dropout(self.fc2, self.keep_prob)
        self.fc3 = slim.fully_connected(self.drop2, num_hidden,
            activation_fn = tf.nn.relu,
            weights_initializer = tf.contrib.layers.xavier_initializer(),
            biases_initializer = tf.zeros_initializer())
        self.drop3 = tf.nn.dropout(self.fc2, self.keep_prob)

        self.prediction = slim.fully_connected(self.drop3, 1,
            activation_fn = None,
            weights_initializer = tf.contrib.layers.xavier_initializer(),
            biases_initializer = None)

        self.cost = tf.reduce_mean(tf.squared_difference(self.target, self.prediction))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.cost)

    def train(self, sess, inp, out, num_epoch):
        if len(inp) == 0:
            return
        for epoch in range(num_epoch):
            avg_cost = 0
            ptr = 0
            for _ in range(num_batches):
                op, c = sess.run([self.optimizer, self.cost], {self.data: np.reshape(inp, [np.shape(inp)[0],1]),\
                    self.target: np.reshape(out, [np.shape(out)[0], 1]),\
                    self.keep_prob: drop_rate})
                avg_cost += c
            avg_cost /= num_batches
            #if self.curr_epoch%100 == 0 and self.curr_epoch != 0:
            #    print self.curr_epoch, avg_cost
            self.curr_epoch += 1

    def predict(self, sess, inp):
        preds = []
        for j in range(num_to_predict):
            preds.append(sess.run(self.prediction, {self.data: np.reshape(inp, [1,1]),\
                self.keep_prob: drop_rate}))
        return np.mean(preds), np.std(preds)

    def test(self, sess, inp):
        Means = np.zeros(len(inp))
        Sdvs = np.zeros(len(inp))
        Results = np.zeros(len(inp))
        for i in range(len(inp)):
            Preds = []
            Results[i] = sess.run(self.prediction, {self.data: np.reshape(inp[i], [1,1]),\
                self.keep_prob: 1})
            for j in range(num_to_predict):
                Preds.append(sess.run(self.prediction, {self.data: np.reshape(inp[i], [1,1]),\
                    self.keep_prob: drop_rate}))
            Means[i] = np.mean(Preds)
            Sdvs[i] = np.std(Preds)
        return Means, Sdvs, Results

class Engine(object):
    def __init__(self):       
        self.net = network()
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        self.reset()

        self.xmin = -2
        self.xmax = 4
        #self.input_memory = np.arange(-2,2,0.001)
        #self.output_memory = self.get_true_value(self.input_memory)
        
        #self.net.train(self.sess, self.input_memory, self.output_memory,00)
        #self.Means, self.Sdvs, self.Predictions = self.net.test(self.sess, np.arange(self.xmin, self.xmax, 0.001))

    def reset(self):
        self.x = 0 #np.random.rand() - 0.5
        self.y = self.get_true_value([self.x])
        self.uncert = 0
        self.sess.run(tf.global_variables_initializer())
        self.net.curr_epoch = 0
        self.input_memory = []
        self.output_memory = []
   
    def get_state(self):
        return np.array([self.x,self.y,self.uncert])     

    def set_state(self, x):
         if x > xmin and x < xmax:
            self.x = x
            self.y, self.uncert = self.engine.get_prediction(self.engine.x) 
       
    def get_prediction(self,x_val):
        pred, std = self.net.predict(self.sess, x_val)
        return pred, std

    def get_true_value(self,x_vals, noise = 0):
        def indv(x):
            fnoise = np.random.uniform(-noise, noise)
            return(np.sin(x * (2*np.pi)) + fnoise)
        vec = [indv(x) + x for x in x_vals]
        return np.array(vec).flatten()

    #TODO only add new data to memory 
    """
    def add_to_memory(self, new_inp, new_out):
        
    """
        
    def add_to_memory(self, new_inp, new_out):
        self.input_memory = np.concatenate([self.input_memory, new_inp])
        self.output_memory = np.concatenate([self.output_memory, new_out])
    
    def train_net(self, num_epochs):
        self.net.train(self.sess, self.input_memory, self.output_memory, num_epochs)

    def test_net(self):
        self.Means, self.Sdvs, self.Predictions = self.net.test(self.sess, np.arange(self.xmin,self.xmax,0.001))
        return self.Means, self.Sdvs

    def plt_trained(self):
        x_range = np.arange(self.xmin,self.xmax,0.001)
        self.test_net()
        plt.clf()
        fig = plt.figure()
        gs = gridspec.GridSpec(2,1, height_ratios = [1,3])
        ax1 = plt.subplot(gs[0])
        plt.plot(x_range, self.Sdvs)
        plt.ylim(ymin = 0, ymax = 2)
        plt.xlim(xmin = self.xmin, xmax = self.xmax)
        plt.ylabel('Abs Uncertainty')
        ax2 = plt.subplot(gs[1])
        plt.plot(x_range, self.get_true_value(x_range), c = 'k', alpha = 0)
        plt.ylim(ymin = plt.ylim()[0], ymax = plt.ylim()[1] + 2)
        plt.xlim(xmin = self.xmin, xmax = self.xmax)
        #plt.plot(x_range, self.Predictions, c = 'g')
        plt.scatter(x_range, self.Means, c = 'r', s = 6)        
        plt.fill_between(x_range, self.Means - self.Sdvs, self.Means + self.Sdvs, facecolor = 'r', alpha = 0.5)
        plt.fill_between(x_range, self.Means - 2*self.Sdvs, self.Means + 2*self.Sdvs, facecolor = 'r', alpha = 0.25)
        plt.fill_between(x_range, self.Means - 3*self.Sdvs, self.Means + 3*self.Sdvs, facecolor = 'r', alpha = 0.1)        
        plt.scatter(self.input_memory, self.output_memory, c = 'b', s = 12)
        plt.plot(x_range, self.get_true_value(x_range), c = 'k')
        savefig('trained')
        

        
