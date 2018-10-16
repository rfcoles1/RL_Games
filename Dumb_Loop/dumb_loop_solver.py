import numpy as np
import gym
import cleangym

game = gym.make('DumbLoop-v0').unwrapped

def choose_move(s):
    x = s[0]
    y = s[1]

    dist_left = abs(x - game.engine.xmin)
    dist_right = abs(x - game.engine.xmax)   
    dist_down = abs(y - game.engine.ymin)
    dist_up = abs(y - game.engine.ymax)

    if dist_left == 0 and dist_up != 0:   
        return 3 #moveup

    if dist_right == 0 and dist_down != 0:
        return 2 #movedown

    if dist_down == 0 and dist_left != 0:
        return 0 #moveright

    if dist_up == 0 and dist_right != 0:
        return 1 #moveleft

    mindist = min([dist_up,dist_down,dist_right,dist_left])

    if dist_left == mindist:
        return 0 #moveleft
    elif dist_right == mindist:
        return 1 #moderight
    elif dist_down == mindist:
        return 2 #moveup
    else:
        return 3 #movedown

    print 'no move'
    return 5

steps = 50
episodes = 2000
moves = []
for j in range(episodes):
    s = game.reset()
    tot_r = 0
    for i in range(50):
        a = choose_move(s)
        moves.append([s[0],s[1],a])
        s,r,d,_ = game.step(a)
        tot_r += r   
  

f_handle = file('ideal_moves.dat', 'a') 
np.savetxt(f_handle, moves)
f_handle.close()
