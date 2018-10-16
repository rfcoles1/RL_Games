import matplotlib.pyplot as plt
import numpy as np
import os 
from pylab import savefig

inputdata = 'ideal_moves.dat' 

x = np.loadtxt(inputdata, dtype = float, usecols = 0)
y = np.loadtxt(inputdata, dtype = float, usecols = 1)

pltx = []
plty = []
fig = plt.figure(1)

def plot_square(xmin,xmax,ymin,ymax):
    plt.plot([xmin,xmax],[ymin,ymin])
    plt.plot([xmin,xmax],[ymax,ymax])
    plt.plot([xmin,xmin],[ymin,ymax])
    plt.plot([xmax,xmax],[ymin,ymax])

for i in range(len(x)):
    pltx.append(x[i])
    plty.append(y[i])

    plt.xlim([0,10])
    plt.ylim([0,10])
    plt.plot(pltx, plty)
    plt.scatter(pltx[-1], plty[-1], c ='red')

    fname = '_trainingvid%05d.png'%(i) 
    savefig(fname, dpi=150)
    plt.clf()

os.system('ffmpeg -r 10 -i _trainingvid%05d.png -vcodec mpeg4 -y loop.mp4')
for i in range(0,len(x)):
    os.remove('_trainingvid%05d.png'%(i))

