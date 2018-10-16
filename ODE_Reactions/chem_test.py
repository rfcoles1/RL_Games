import numpy as np
import gym
import ChemGym
import matplotlib.pyplot as plt

env = gym.make('Reaction-v0').unwrapped
state = env.reset()
print state
actions = []
steps = []
A = []
B = []
C = []
k1 = []
k2 = []
k3 = []

for i in range(100):
    state,_,_,_ = env.step(6)
    A.append(state[0])
    B.append(state[1])
    C.append(state[2])
    k1.append(state[3])
    k2.append(state[4])
    k3.append(state[5])

plt.figure(1)
plt.plot(A,c = 'r')
plt.plot(B,c = 'b')
plt.plot(C,c = 'g')
plt.figure(2)
plt.plot(k1,c = 'r')
plt.plot(k2,c = 'b')
plt.plot(k3,c = 'g')

plt.show()

