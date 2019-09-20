import numpy as np
import gym 
from heat_engine import Engine

class HeatEnv(gym.Env):
    def __init__(self):
        self.engine = Engine()
        self.done = False
        
        self.TargetMass = np.array([0,.5,.5])
        self.TargetTemp = 100
    
        self.action_space = gym.spaces.Box(low=-1., high=1., shape=(1,), dtype=np.float32)
        self.reset()

    def reset(self):
        self.engine.reset()
        return self.engine.get_state()

    def get_state(self):
        return self.engine.get_state()

    def step(self, action):
        self.add_energy(action)
        next_state = self.engine.get_state()
        reward = self.get_reward()
        return next_state, reward, self.done, {}

    def add_energy(self, action):
        action = np.clip(action,-1,1)
        energy = (action)*100
        self.engine.EnergyIn += energy
        self.engine.set_Temp()

    def get_reward(self):
        state = self.engine.get_state()
        msd = abs(state[3] - self.TargetTemp)
        return -msd 

    def render(self, mode = 'human'):
        return 0 


