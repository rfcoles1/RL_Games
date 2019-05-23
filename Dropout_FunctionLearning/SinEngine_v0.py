import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

num_hidden = 512
batch_size = 100
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
            biases_initializer = tf.ones_initializer())
        self.drop2 = tf.nn.dropout(self.fc2, self.keep_prob)
        self.fc3 = slim.fully_connected(self.drop2, num_hidden,
            activation_fn = tf.nn.relu,
            weights_initializer = tf.contrib.layers.xavier_initializer(),
            biases_initializer = tf.ones_initializer())
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
        num_batches = int(len(inp)/batch_size)
        for epoch in range(num_epoch):
            avg_cost = 0
            ptr = 0
            for _ in range(num_batches):
                inp_batch = inp[ptr:ptr+batch_size]
                out_batch = out[ptr:ptr+batch_size]
                ptr += batch_size
                op, c = sess.run([self.optimizer, self.cost], {self.data: np.reshape(inp_batch, [np.shape(inp_batch)[0],1]),\
                    self.target: np.reshape(out_batch, [np.shape(out_batch)[0], 1]),\
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
        self.sess = tf.Session(config=tf.ConfigProto(use_per_session_threads=True))
        
        self.reset()

        self.xmin = -2
        self.xmax = 8
        
    def reset(self):
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
        
    def add_to_memory(self, new_inp, new_out):
        self.input_memory = np.concatenate([self.input_memory, new_inp])
        self.output_memory = np.concatenate([self.output_memory, new_out])    

    def train_net(self, num_epochs):
        self.net.train(self.sess, self.input_memory, self.output_memory, num_epochs)

    def test_net(self,):
        self.Means, self.Sdvs, self.Predictions = self.net.test(self.sess, np.arange(self.xmin,self.xmax,0.01))
        return self.Means, self.Sdvs

