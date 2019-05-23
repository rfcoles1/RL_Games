import numpy as np
import gym
from sineng import Engine

class SinEnv(gym.Env):
    def __init__(self):
        self.engine = Engine()
        self.done = False

        self.target = 3
        self.incr = 0.1

        self.action_space = gym.spaces.Discrete(4)
        self.reset()

    def reset(self):
        self.num_trained = 0
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
            
        new_y = self.engine.get_true_value(new_x)
        self.engine.add_to_memory(new_x, new_y)
        self.engine.train_net(1000)

        self.engine.y, self.engine.uncert = self.engine.get_prediction(self.engine.x)

    def get_reward(self):
        state = self.engine.get_state()
        msd = abs(self.engine.y - self.target)
        return -msd - state[2]

    def render(self, mode = 'human'):
        return 0

