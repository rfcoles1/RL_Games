import numpy as np
import matplotlib.pyplot as plt
from SinGame_v1 import SinEnv2

E = SinEnv2()

def print_status():
    print 'number of times data is obtained: ' + str(E.num_obs)
    print 'number of epochs trained: ' + str(E.engine.net.curr_epoch)
    print 'env state: ' + str([E.engine.x, E.get_true_value([E.engine.x])])
    print 'SE state: ' + str(E.engine.get_state())
    print 'Rewad: ' + str(E.get_reward())

def print_memory():
    print 'input:' + str(len(E.engine.input_memory))
    print E.engine.input_memory
    print 'output:' + str(len(E.engine.output_memory))
    print E.engine.output_memory
