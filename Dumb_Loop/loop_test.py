import matplotlib.pyplot as plt
import numpy as np
import gym
import cleangym

lp = gym.make('DumbLoop-v0').unwrapped
lp.reset()
actions = [1,3]

print lp.action_space.n

xs = [lp.engine.x]
ys = [lp.engine.y]

for action in (actions):
    
    lp.step(action)
    xs.append(lp.engine.x)
    ys.append(lp.engine.y)

plt.figure(1)
plt.xlim(xmin = lp.engine.xmin, xmax = lp.engine.xmax)
plt.ylim(ymin = lp.engine.ymin, ymax = lp.engine.ymax)
plt.plot(xs,ys)
plt.show()

