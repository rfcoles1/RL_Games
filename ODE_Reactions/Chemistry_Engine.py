import numpy as np

def rk4(r,t,h):
    k1 = h*f(r,t)
    k2 = h*f(r+0.5*k1, t+0.5*h)
    k3 = h*f(r+0.5*k2, t+0.5*h)
    k4 = h*f(r+k3,t+h)
    return (k1+2*k2+2*k3+k4)/6.0

class Engine(object):
    def __init__(self, num_rates, num_species):
        self.timelimit = 5
        self.timestep = 0.01
        self.maxK = 2
        self.minK = 0
        self.increment = 0.01
        self.num_rates = num_rates
        self.num_species = num_species
        self.reset()

    def set_rates(self, new_rates):
        for i in range(len(new_rates)):
            self.rates[i] = new_rates[i]
 
    def set_species(self, new_species):
        for i in range(len(new_species)):
            self.species[i] = new_species[i]

    def set_state(self, new_state):
        species = new_state[:self.num_species]
        rates = new_state[self.num_species:]
        self.species = species
        self.rates = rates

    def get_state(self):
        return np.concatenate([self.species,self.rates])

    def reset(self):
        self.rates = np.zeros(self.num_rates)
        self.species = np.zeros(self.num_species)

    def change_rates(self, num_rates, action):
        for i in range(0, num_rates):
            if (action == i) & (self.rates[i] < self.maxK):
                self.rates[i] += self.increment
                break
            elif (action == (i + num_rates)) & (self.rates[i] > self.minK):
                self.rates[i] -= self.increment
                break
"""               
    def run_step(self,f):
        return 0 
"""
