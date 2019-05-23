import numpy as np
import gym

#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#from pylab import savefig

from WaterEngine import Engine

import time 

LatentHeat_Fusion = 334 #kJ/kg
LatentHeat_Vapor = 2264.705 #kJ/kg
MeltingPoint = 0 #degC
BoilingPoint = 100.0 #degC
HeatCap_Ice = 2.108 #kJ/kg/C
HeatCap_Water = 4.148 #kJ/kg/C
HeatCap_Steam = 1.996 #kJ/kg/C


class BoilEnv(gym.Env):
    def __init__(self, T = 21, M = 1):
        self.engine = Engine()
        self.done = False

        self.Ti = T
        self.M = M

        self.TargetTemp = 100 #target y value the function
        self.TargetMass = np.array([0,0.5,0.5])
        self.incr = 0.1 #how much energy the agent can add in one step

        self.action_space = gym.spaces.Discrete(5)
 
        self.gen_critPoints(self.Ti)
        self.reset()

    def get_true_value(self, E):
        if E > self.Upper_Boiling_Energy:
            T = BoilingPoint + (1./HeatCap_Steam)*(self.engine.EnergyIn-self.Upper_Boiling_Energy)
            MassFractions = [0,0,1]
            return T, MassFractions
        elif E > self.Lower_Boiling_Energy:
            T = BoilingPoint
            Ediff = self.engine.EnergyIn - self.Lower_Boiling_Energy
            MassFractions = [0, Ediff/LatentHeat_Vapor, 1. - Ediff/LatentHeat_Vapor]
            return T, MassFractions
        elif E > self.Upper_Melting_Energy:
            T = MeltingPoint + (1./HeatCap_Water)*(self.engine.EnergyIn-self.Upper_Melting_Energy)
            MassFractions = [0,1,0]
            return T, MassFractions
        elif E > self.Lower_Melting_Energy:
            T = MeltingPoint
            Ediff = self.engine.EnergyIn - self.Lower_Melting_Energy
            MassFractions = [Ediff/LatentHeat_Fusion, 1. - Ediff/LatentHeat_Fusion,0]
            return T, MassFractions
        else:
            T = self.Ti + (1./HeatCap_Ice)*self.engine.EnergyIn
            MassFractions = [1,0,0]
            return T, MassFractions

    def reset(self):
        self.num_obs = 0
        self.engine.EnergyIn = 0
        self.engine.Temp, self.engine.MassFractions = self.get_true_value(self.engine.EnergyIn)
        self.engine.Terr, self.engine.Merr = 0, 0 
        self.engine.reset()
        #self.gain()
        #for _ in range(1):#10 to keep it consistent 
        #self.train()
        return self.engine.get_state()

    def get_state(self):
        return self.engine.get_state()

    def step(self, action):
        self.do_action(action)
        next_state = self.engine.get_state()
        reward = self.get_reward()
        return next_state, reward, self.done, {}
 
    """   
    action 0: move left
    action 1: no move
    action 2: move right
    action 3: get more data
    action 4: train on current data
    """

    def do_action(self,action):
        if action == 3:
            #if self.num_obs < 10:
            #    self.gain() 
            #    self.num_obs += 1
            self.gain()
            return
        if action == 4:
            self.train()
            self.engine.Temp, self.engine.Terr, self.engine.MassFractions, self.engine.Merr = self.engine.get_prediction(self.enging.EnergyIn)
            return

        self.engine.EnergyIn += (action-1)*self.incr
 
        if action != 1:
            self.engine.Temp, self.engine.Terr, self.engine.MassFractions, self.engine.Merr = self.engine.get_prediction(self.engine.EnergyIn)

    def gain(self):
        width = 0.25
        new_E = []
        
        currE = self.engine.EnergyIn - width

        while currE < self.engine.EnergyIn + width:
            new_E.append(currE)
            currE += 0.001
            
        new_Temp, new_MassFrac = self.get_true_value(new_E)
        self.engine.add_to_memory(new_E, [[new_Temp], new_MassFrac])        
        
    def train(self):     
        self.engine.train_net(100)
        self.engine.Temp, self.engine.T_err, self.engine.MassFractions, self.engine.Merr = self.engine.get_prediction(self.engine.EnergyIn)

    def get_reward(self):
        state = self.engine.get_state()
        true_T, true_M = self.get_true_value(self.EnergyIn)
        msd_true = abs(true_y - self.target)
        msd_fake = abs(state[1] - self.target)
        return -msd_fake - msd_true - state[2] 

    def render(self, mode = 'human'):
        return 0

    def plt_trained(self):
        x_range = np.arange(self.engine.xmin,self.engine.xmax,0.01)
        self.engine.test_net()
        plt.clf()
        #fig = plt.figure()
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
        plt.show()                              

    def gen_critPoints(self, T):
        self.Upper_Melting_Energy = (MeltingPoint - T) * HeatCap_Water
        self.Lower_Melting_Energy = self.Upper_Melting_Energy - LatentHeat_Fusion

        self.Lower_Boiling_Energy = (BoilingPoint - T) * HeatCap_Water
        self.Upper_Boiling_Energy = self.Lower_Boiling_Energy + LatentHeat_Vapor

