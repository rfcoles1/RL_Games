import numpy as np

LatentHeat_Fusion = 334 #kJ/kg
LatentHeat_Vapor = 2264.705 #kJ/kg
MeltingPoint = 0 #degC
BoilingPoint = 100.0 #degC
HeatCap_Ice = 2.108 #kJ/kg/C
HeatCap_Water = 4.148 #kJ/kg/C
HeatCap_Steam = 1.996 #kJ/kg/C

class Engine(object):
    def __init__(self, T = 21, M = 1):
        self.Ti = T #degC
        self.RoomTemp = 21
        self.Mass = M #Kg
        self.Time_interval = 0.1 #seconds
        self.reset()
        self.gen_true(21)

    def reset(self):
        self.T = self.Ti
        self.MassFractions = np.array([0,1,0])
        self.EnergyIn = 0

    def set_MassFrac(self, Ice, Water, Steam):
        self.MassFractions = np.array([Ice, Water, Steam])

    def get_state(self):
        return np.append(self.MassFractions, self.T)
    
    def set_Temp(self):
        if self.EnergyIn > self.Upper_Boiling_Energy:
            self.T = BoilingPoint + (1./HeatCap_Steam)*(self.EnergyIn-self.Upper_Boiling_Energy)
            self.MassFractions = [0,0,1]
        elif self.EnergyIn > self.Lower_Boiling_Energy:
            self.T = BoilingPoint
            Ediff = self.EnergyIn - self.Lower_Boiling_Energy
            self.MassFractions = [0, 1. - Ediff/LatentHeat_Vapor, Ediff/LatentHeat_Vapor]
        elif self.EnergyIn > self.Upper_Melting_Energy:
            self.T = MeltingPoint + (1./HeatCap_Water)*(self.EnergyIn-self.Upper_Melting_Energy)
            self.MassFractions = [0,1,0]
        elif self.EnergyIn > self.Lower_Melting_Energy:
            self.T = MeltingPoint
            Ediff = self.EnergyIn - self.Lower_Melting_Energy
            self.MassFractions = [1. - Ediff/LatentHeat_Fusion, Ediff/LatentHeat_Fusion,0]
        else:
            self.T = self.Ti + (1./HeatCap_Ice)*self.EnergyIn
            self.MassFractions = [1,0,0]

    def gen_true(self, T):    
        self.Upper_Melting_Energy = (MeltingPoint - self.T) * HeatCap_Water
        self.Lower_Melting_Energy = self.Upper_Melting_Energy - LatentHeat_Fusion

        self.Lower_Boiling_Energy = (BoilingPoint - self.T) * HeatCap_Water
        self.Upper_Boiling_Energy = self.Lower_Boiling_Energy + LatentHeat_Vapor



