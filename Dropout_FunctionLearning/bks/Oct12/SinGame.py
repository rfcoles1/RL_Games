import numpy as np
import gym
from SinEngine import Engine

class SinEnv(gym.Env):
    def __init__(self):
        self.engine = Engine()
        self.done = False

        self.target = 3 #target y value the function
        self.incr = 0.1 #how much the agent can move in the x direction

        self.action_space = gym.spaces.Discrete(4)
        self.reset()

    def get_true_value(self, x_vals, noise = 0):
        def indv(x):
            fnoise = np.random.uniform(-noise, noise)
            return(np.sin(x * (2*np.pi) + fnoise))
        vec = [indv(x) + x for x in x_vals]
        return np.array(vec).flatten()
    
    def reset(self):
        self.num_trained = 0
        self.engine.x = 0
        self.engine.y = self.get_true_value([self.engine.x])
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
        if action == 3:
            if self.num_trained < 10:
                self.gain_knowledge() 
                self.num_trained += 1
            return
        
        self.engine.x += (action-1)*self.incr
        if self.engine.x < self.engine.xmin:
            self.engine.x = self.engine.xmin
        if self.engine.x > self.engine.xmax:
            self.engine.x = self.engine.xmax
 
        self.engine.y, self.engine.uncert = self.engine.get_prediction(self.engine.x)

    def gain_knowledge(self):
        width = 0.25
        new_x = []
        
        currx = self.engine.x - width
        if currx < self.engine.xmin:
            currx = self.engine.xmin

        while currx < self.engine.x + width:
            if currx > self.engine.xmax:
                break
            new_x.append(currx)
            currx += 0.001
            
        new_y = self.get_true_value(new_x)
        self.engine.add_to_memory(new_x, new_y)
        self.engine.train_net(1000)

        self.engine.y, self.engine.uncert = self.engine.get_prediction(self.engine.x)

    def get_reward(self):
        state = self.engine.get_state()
        msd = abs(self.engine.y - self.target)
        return -msd - state[2]

    def render(self, mode = 'human'):
        return 0

    def plt_trained(self):
        x_range = np.arange(self.engine.xmin,self.engine.xmax,0.001)
        self.engine.test_net()
        plt.clf()
        fig = plt.figure()
        gs = gridspec.GridSpec(2,1, height_ratios = [1,3])
        ax1 = plt.subplot(gs[0])
        plt.plot(x_range, self.engine.Sdvs)
        plt.ylim(ymin = 0, ymax = 2)
        plt.xlim(xmin = self.engine.xmin, xmax = self.engine.xmax)
        plt.ylabel('Abs Uncertainty')
        ax2 = plt.subplot(gs[1])
        plt.plot(x_range, self.get_true_value(x_range), c = 'k', alpha = 0)
        plt.ylim(ymin = plt.ylim()[0], ymax = plt.ylim()[1] + 2)
        plt.xlim(xmin = self.engine.xmin, xmax = self.engine.xmax)
        #plt.plot(x_range, self.Predictions, c = 'g')
        plt.scatter(x_range, self.engine.Means, c = 'r', s = 6)
        plt.fill_between(x_range, self.engine.Means - self.engine.Sdvs, self.engine.Means + self.engine.Sdvs,\
            facecolor = 'r', alpha = 0.5)
        plt.fill_between(x_range, self.engine.Means - 2*self.engine.Sdvs, self.engine.Means + 2*self.engine.Sdvs,\
            facecolor = 'r', alpha = 0.25)
        plt.fill_between(x_range, self.engine.Means - 3*self.engine.Sdvs, self.engine.Means + 3*self.engine.Sdvs,\
            facecolor = 'r', alpha = 0.1) 
        plt.scatter(self.engine.input_memory, self.engine.output_memory, c = 'b', s = 12)
        plt.plot(x_range, self.get_true_value(x_range), c = 'k')
                                          

