import numpy as np
import gym
from Chemistry_Engine import Engine

"""
A + B --k1--> F
A + C --k2--> G
F + G --k3--> X
"""

def rk4(r,t,h):
    k1 = h*f(r,t)
    k2 = h*f(r+0.5*k1, t+0.5*h)
    k3 = h*f(r+0.5*k2, t+0.5*h)
    k4 = h*f(r+k3, t*h)
    return (k1+2*k2+2*k3+k4)/6.0

def f(r,t):
    A = r[0]
    B = r[1]
    C = r[2]
    F = r[3]
    G = r[4]
    X = r[5]

    k1 = r[6]
    k2 = r[7]
    k3 = r[8]

    fA = -k1*A*B - k2*A*C
    fB = -k1*A*B
    fC = -k2*A*C
    fF = k1*A*B -k3*F*G
    fG = k2*A*C  + -k3*F*G
    fX = k3*F*G

    return np.array([fA, fB, fC, fF, fG, fX, 0, 0, 0], float)

class Reaction_Env(gym.Env):
    def __init__(self):
        self.num_rates = 3
        self.num_species = 6

        self.engine = Engine(self.num_rates, self.num_species)
        self.done = False
       
        self.action_space = gym.spaces.Discrete(self.num_rates*2 + 1)

    def reset(self):
        self.engine.reset()
        self.engine.set_species([100,100,100,0,0,0])
        self.engine.set_rates([1,1,1])
        return self.engine.get_state()

    def step(self,action):
        curr_state = self.engine.get_state()
        self.engine.change_rates(self.num_rates,action)
        reward = self.run_react()
        next_state = self.engine.get_state()
        
        return next_state, reward, self.done, {}

    def render(self, mode='human'):
        return 0

    def run_react(self):
        h = 0.0033
        t = 0
        timestep = self.engine.timestep
        
        r = self.engine.get_state()
        
        while t<timestep:
            t += h
            r += rk4(r,t,h)
        self.engine.set_state(r) 
        return r[2]#product in this reaction is D


