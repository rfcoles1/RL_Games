import numpy as np

class Droplet(object):
    def __init__(self, name, species, color = -1):
        self.state = np.array(species)#species is defined by array of all possible species
        self.name = name
        if color == -1:
            self.color = np.random.rand(3)
        else:
            self.color = color

    def __repr__(self):
        return str(self.name)

    def return_last_true(self): #returns the name and state of the drop at the last known instance 
        tmp_name = self.name.split('|',1)[0]       

        if np.ndim(self.state) == 1:#if only one list of species, it is true representation of that drop
            return tmp_name, self.state
        else: #return the first species array 
            return tmp_name, self.state[0]

    def combine(self,drop): #combines a drop without resolving
        self.name = self.name + '|' + drop.name
        self.state = np.vstack([self.state,drop.state])
        self.color = 0.5*(self.color + np.array(drop.color))

    def resolve(self):
        return 0
    
    def create_mix(self,drop): #if two drops form a mixture, then the species are simply summed
        self.name = self.name + ',' + drop.name
        for i in range(len(self.state)):
            self.state[i] += drop.state[i]
            self.color += drop.color[i]
        
