import numpy as np
import gym
from FunctionEngine_2D import Engine

class FuncEnv(gym.Env):
    def __init__(self):
        self.engine = Engine()
        self.done = False

        self.target = 3 #target y value the function
        self.incr = 0.1 #how much the agent can move in the x direction

        self.action_space = gym.spaces.Discrete(6)
        self.reset()

    def get_true_value(self, new_inp):
        new_inp = np.array(new_inp)
        if new_inp.ndim == 1:
            new_inp = np.reshape(new_inp, [1,self.engine.input_dims])
        x_vals = new_inp[:,0]
        y_vals = new_inp[:,1]
        return 20 + x_vals**2 + y_vals**2 - 10*(np.cos(2*np.pi*x_vals) + np.cos(2*np.pi*y_vals))
          
    def reset(self):
        self.num_trained = 0
        self.engine.x = 0
        self.engine.y = 0
        self.engine.z = self.get_true_value([self.engine.x,self.engine.y])
        self.engine.uncert = 0
        self.engine.reset()
        self.gain_knowledge()
        return self.engine.get_state()

    def get_state(self):
        return self.engine.get_state()

    def step(self, action):
        self.do_action(action)
        next_state = self.engine.get_state()
        reward = self.get_reward()
        return next_state, reward, self.done, {}
    
    def do_action(self,action):
        if action == 0:
            if self.num_trained < 10:
                self.gain_knowledge() 
                self.num_trained += 1
            return
        
        if action == 1:
            if self.engine.x < self.engine.xmax:
                self.engine.x += self.incr        
        elif action == 2:
            if self.engine.x > self.engine.xmin:
                self.engine.x -= self.incr
        elif action == 3:
            if self.engine.y < self.engine.ymax:
                self.engine.y += self.incr
        elif action == 4:
            if self.engine.y > self.engine.ymin:
                self.engine.y -= self.incr

        #nothing happens on action 5

        self.engine.z, self.engine.uncert = self.engine.get_prediction([self.engine.x, self.engine.y])

    def gain_knowledge(self):
        width = 0.25
        new_inp = []
         
        currx = self.engine.x - width
        if currx < self.engine.xmin:
            currx = self.engine.xmin
        
        ylen = 0
        direct = 1

        while currx <= self.engine.x + width:
            curry = self.engine.y - ylen
            while curry <= self.engine.y + ylen:
                new_inp.append([currx,curry])
                curry += 0.001
            currx += 0.001
            ylen += direct*0.001
            if currx >= 0:
                direct = -1

        new_z = self.get_true_value(new_inp)
        self.engine.add_to_memory(new_inp, new_z)
        self.engine.train_net(1000)

        self.engine.z, self.engine.uncert = self.engine.get_prediction([self.engine.x,self.engine.y])

    def get_reward(self):
        state = self.engine.get_state()
        msd = abs(self.engine.y - self.target)
        return -msd - state[2]

    def render(self, mode = 'human'):
        return 0

    def plt_trained(self):
        x_range = np.arange(self.engine.xmin,self.engine.xmax,0.001)
        y_range = np.arange(self.engine.ymin,self.engine.ymax,0.001)
        self.engine.test_net()
        plt.clf()
        fig = plt.figure()
        gs = gridspec.GridSpec(1,2, height_ratios = [1,1])
        ax1 = plt.subplot(gs[1])
        #plt.imshow()
        #plt.ylim(ymin = 0, ymax = 2)
        #plt.xlim(xmin = self.engine.xmin, xmax = self.engine.xmax)
        plt.xlabel('Abs Uncertainty')
        ax2 = plt.subplot(gs[0])
        plt.imshow()
        #plt.ylim(ymin = plt.ylim()[0], ymax = plt.ylim()[1] + 2)
        #plt.xlim(xmin = self.engine.xmin, xmax = self.engine.xmax)
        #plt.plot(x_range, self.Predictions, c = 'g')
        plt.scatter(x_range, self.engine.Means, c = 'r', s = 6)
        plt.scatter(self.engine.input_memory, self.engine.output_memory, c = 'b', s = 12)
        plt.plot(x_range, self.get_true_value(x_range), c = 'k')
                                          

