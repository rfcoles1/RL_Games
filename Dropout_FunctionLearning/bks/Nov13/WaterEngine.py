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
            biases_initializer = tf.zeros_initializer())
        self.drop1 = tf.nn.dropout(self.fc1, self.keep_prob)
        self.fc2 = slim.fully_connected(self.drop1, num_hidden,
            activation_fn = tf.nn.relu,
            weights_initializer = tf.contrib.layers.xavier_initializer(),
            biases_initializer = tf.zeros_initializer())
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
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        self.reset()
        
    def reset(self):
        self.sess.run(tf.global_variables_initializer())
        self.net.curr_epoch = 0
        self.input_memory = []
        
        self.output_memory = np.empty_like([[0], [1,1,1]])

    def get_state(self):
        return np.array([self.EnergyIn, self.Temp, self.Terr, self.MassFractions, self.Merr])     

    def set_state(self, E):
        self.EnergyIn = E
        self.Temp, self.Terr, self.MassFractions, self.Merr = self.get_prediction(self.engine.EnergyIn) 
       
    def get_prediction(self,E_vals):
        Tpred, Tstd, Mpred, Mstd = self.net.predict(self.sess, x_val)
        return Tpred, Tstd, Mpred, Mstd
        
    def add_to_memory(self, new_inp, new_out):
        self.input_memory = np.concatenate([self.input_memory, new_inp])
        self.output_memory = np.concatenate([self.output_memory, new_out])
    
    def train_net(self, num_epochs):
        self.net.train(self.sess, self.input_memory, self.output_memory, num_epochs)

    def test_net(self,):
        self.Means, self.Sdvs, self.Predictions = self.net.test(self.sess, np.arange(self.xmin,self.xmax,0.01))
        return self.Means, self.Sdvs

    def gen_critPoints(self, T):
        self.Upper_Melting_Energy = (MeltingPoint - self.T) * HeatCap_Water
        self.Lower_Melting_Energy = self.Upper_Melting_Energy - LatentHeat_Fusion

        self.Lower_Boiling_Energy = (BoilingPoint - self.T) * HeatCap_Water
        self.Upper_Boiling_Energy = self.Lower_Boiling_Energy + LatentHeat_Vapor

